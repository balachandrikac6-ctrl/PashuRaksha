import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from backend.main import calculate_risk, init_db

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "backend" / "pashuraksha.db"

ROLE_OPTIONS = ["Farmer", "Veterinary", "Government"]
PORTAL_MODULES = {
    "Farmer": [
        ("health", "🩺", "animal_health", "animal_health_desc"),
        ("appointments", "📅", "appointments_module", "appointments_desc"),
        ("reports", "📋", "reports_module", "reports_desc"),
        ("notifications", "🔔", "notifications_module", "notifications_desc"),
        ("care", "🌿", "animal_care_module", "animal_care_desc"),
    ],
    "Veterinary": [
        ("animal_reports", "📊", "animal_reports_module", "animal_reports_desc"),
        ("appointment_requests", "🚑", "appointment_requests_module", "appointment_requests_desc"),
        ("laboratory", "🔬", "laboratory_module", "laboratory_desc"),
        ("notifications", "🔔", "notifications_module", "notifications_desc"),
    ],
    "Government": [
        ("animal_reports", "📋", "animal_reports_module", "animal_reports_desc"),
        ("village_risk", "🏘️", "village_risk_module", "village_risk_desc"),
        ("risk_management", "📈", "risk_management_module", "risk_management_desc"),
        ("notifications", "🔔", "notifications_module", "notifications_desc"),
    ],
}
ANIMAL_OPTIONS = [
    "Cow", "Buffalo", "Goat", "Sheep", "Chicken", "Duck", "Pig", "Dog",
    "Cat", "Horse", "Donkey", "Camel", "Rabbit", "Turkey", "Pigeon",
]

SYMPTOMS = [
    "fever", "cough", "diarrhea", "vomiting", "not_eating", "reduced_eating",
    "weakness", "lethargy", "difficulty_breathing", "nasal_discharge", "eye_discharge",
    "swelling", "skin_lesions", "itching", "hair_loss", "wounds", "lameness",
    "abdominal_swelling", "bloating", "mouth_sores", "excessive_salivation",
    "milk_drop", "abnormal_milk", "weight_loss", "constipation", "tremors",
    "seizures", "bleeding", "high_thirst", "frequent_urination", "reproductive_problem",
    "ticks", "dehydration", "discharge",
]

CARE_GROUP_BY_ANIMAL = {
    "Cow": "ruminant", "Buffalo": "ruminant", "Goat": "ruminant", "Sheep": "ruminant", "Camel": "ruminant",
    "Chicken": "poultry", "Duck": "poultry", "Turkey": "poultry", "Pigeon": "poultry",
    "Pig": "swine", "Dog": "companion", "Cat": "companion", "Horse": "equine", "Donkey": "equine", "Rabbit": "rabbit",
}

CARE_TOPICS_BY_GROUP = {
    "ruminant": ["general", "digestive", "respiratory", "skin", "injury", "bloat", "udder", "reproductive", "neurological", "toxin"],
    "poultry": ["general", "digestive", "respiratory", "skin", "injury", "flock", "egg", "neurological", "toxin"],
    "swine": ["general", "digestive", "respiratory", "skin", "injury", "bloat", "reproductive", "neurological", "toxin"],
    "companion": ["general", "digestive", "respiratory", "skin", "injury", "urinary", "reproductive", "neurological", "toxin"],
    "equine": ["general", "digestive", "respiratory", "skin", "injury", "colic", "reproductive", "neurological", "toxin"],
    "rabbit": ["general", "digestive", "respiratory", "skin", "injury", "rabbit_gi", "dental", "neurological", "toxin"],
}

CARE_TOPIC_TITLE_KEYS = {
    "general": "general_warning", "digestive": "digestive_warning", "respiratory": "respiratory_warning",
    "skin": "skin_warning", "injury": "injury_warning", "bloat": "care_bloat_title", "udder": "milk_warning",
    "reproductive": "care_reproductive_title", "neurological": "neurological_warning", "toxin": "care_toxin_title",
    "flock": "care_flock_title", "egg": "care_egg_title", "urinary": "care_urinary_title", "colic": "care_colic_title",
    "rabbit_gi": "care_rabbit_gi_title", "dental": "care_dental_title",
}

CARE_TOPIC_SYMPTOMS = {
    "general": ["fever", "not_eating", "weakness"], "digestive": ["diarrhea", "vomiting", "dehydration"],
    "respiratory": ["cough", "difficulty_breathing", "nasal_discharge"], "skin": ["itching", "ticks", "skin_lesions"],
    "injury": ["wounds", "swelling", "lameness"], "bloat": ["abdominal_swelling", "bloating"],
    "udder": ["milk_drop", "abnormal_milk"], "reproductive": ["reproductive_problem", "discharge"],
    "neurological": ["tremors", "seizures"], "toxin": ["vomiting", "tremors", "seizures"],
    "flock": ["cough", "difficulty_breathing", "diarrhea", "weakness"], "egg": ["reduced_eating", "weakness", "discharge"],
    "urinary": ["frequent_urination", "high_thirst", "discharge"], "colic": ["abdominal_swelling", "bloating", "constipation"],
    "rabbit_gi": ["not_eating", "reduced_eating", "abdominal_swelling"], "dental": ["not_eating", "reduced_eating", "weight_loss"],
}

LANGUAGE_CODES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Kannada": "kn-IN",
    "Marathi": "mr-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
}

TRANSLATIONS = {
    "English": {
        "yes": "Yes", "no": "No",
        "respiratory_warning": "Respiratory illness warning", "digestive_warning": "Digestive illness / dehydration warning", "skin_warning": "Skin or external parasite warning", "injury_warning": "Injury or inflammation warning", "general_warning": "General illness / nutrition warning", "milk_warning": "Milk production / udder health warning", "neurological_warning": "Neurological warning", "no_pattern": "No specific condition pattern detected",
        "care_clean_water": "Provide clean drinking water and keep the animal in a clean, comfortable and shaded area.", "care_dehydration": "Watch closely for dehydration and contact a veterinarian if symptoms continue or worsen.", "care_breathing": "Difficulty breathing can be urgent. Seek veterinary care promptly.", "care_urgent": "This may require urgent veterinary attention.", "care_wound": "Keep wounds clean and prevent the animal from further injuring the area.", "care_ticks": "Separate the affected animal when appropriate and ask a veterinarian about safe parasite control.", "care_vet": "Veterinary examination is strongly recommended.", "care_no_medicine": "Do not give prescription medicines without veterinary guidance.",
        "open_module": "Open {title}", "appointment_success": "Appointment request submitted.", "no_appointments": "No appointments available.",
        "status_label": "Status", "status_pending": "Pending", "status_approved": "Approved", "status_rejected": "Rejected",
        "lab_result": "Examination result", "medicine": "Veterinary instructions", "follow_up": "Follow-up required", "notes": "Notes",
        "app_name": "PashuRaksha",
        "subtitle": "Livestock Health & Safety",
        "landing_title": "Protecting Livestock. Protecting Communities.",
        "welcome": "Welcome",
        "full_name": "Full name",
        "mobile": "Phone number",
        "continue": "Open portal",
        "profile_required": "Enter your name and phone number to continue.",
        "choose_portal": "Choose Your Portal",
        "farmer": "Farmer",
        "veterinarian": "Veterinarian",
        "government": "Government",
        "farmer_portal": "Farmer Portal",
        "veterinarian_portal": "Veterinarian Portal",
        "government_portal": "Government Portal",
        "farmer_desc": "Report sick animals and check village health",
        "veterinarian_desc": "Manage cases and respond to health alerts",
        "government_desc": "Monitor villages, risks and livestock health information",
        "back_to_profile": "Back to Profile",
        "read_aloud": "Read Aloud",
        "select_all": "Select All",
        "clear_selection": "Clear",
        "animal_health_report": "Animal Health Report",
        "village_health": "Village Health",
        "health_alerts": "Health Alerts",
        "previous_reports": "Previous Reports",
        "report_another": "Report Another Animal",
        "submit_report": "Submit Health Report",
        "submit_success": "Health report submitted successfully.",
        "symptoms": "Symptoms",
        "days_sick": "Days sick",
        "village": "Village",
        "risk_score": "Risk Score",
        "health_condition": "Health Condition",
        "health_advice": "Health Advice",
        "possible_conditions": "Possible Conditions",
        "disease_risk_prediction": "Disease Risk Prediction",
        "reported_animal": "Reported Animal",
        "detected_symptoms": "Detected Symptoms",
        "time": "Time",
        "risk_level": "Risk Level",
        "disclaimer": "This is a symptom-based health risk assessment and not a professional veterinary diagnosis.",
        "total_reports": "Total Reports",
        "high_risk_cases": "High Risk Cases",
        "medium_risk_cases": "Medium Risk Cases",
        "low_risk_cases": "Low Risk Cases",
        "total_villages": "Total Villages",
        "recent_reports": "Recent Reports",
        "village_summary": "Village Health Summary",
        "report_status": "Submitted Animal Reports",
        "validation_missing_village": "Please enter a village name.",
        "validation_missing_symptoms": "Please select at least one symptom.",
        "validation_missing_animals": "Please select at least one animal.",
        "village_risk": "Village Risk",
        "alert_summary": "Health Alerts",
        "response_note": "Response Note",
        "save_response": "Save Response",
        "completed": "Reviewed",
        "low_risk": "LOW RISK",
        "medium_risk": "MEDIUM RISK",
        "high_risk": "HIGH RISK",
        "no_reports": "No reports available.",
        "no_alerts": "No health alerts.",
        "animal_selection": "Animal selection",
    },
    "Hindi": {
        "yes": "हाँ", "no": "नहीं",
        "respiratory_warning": "श्वसन बीमारी की चेतावनी", "digestive_warning": "पाचन / निर्जलीकरण की चेतावनी", "skin_warning": "त्वचा या परजीवी चेतावनी", "injury_warning": "चोट या सूजन की चेतावनी", "general_warning": "सामान्य बीमारी / पोषण चेतावनी", "milk_warning": "दूध उत्पादन / थन स्वास्थ्य चेतावनी", "neurological_warning": "तंत्रिका संबंधी चेतावनी", "no_pattern": "कोई विशिष्ट स्थिति पैटर्न नहीं मिला",
        "care_clean_water": "साफ पानी दें और पशु को स्वच्छ, आरामदायक और छायादार जगह पर रखें।", "care_dehydration": "निर्जलीकरण पर नज़र रखें और लक्षण जारी रहने या बिगड़ने पर पशु चिकित्सक से संपर्क करें।", "care_breathing": "साँस लेने में कठिनाई आपात स्थिति हो सकती है। तुरंत पशु चिकित्सा सहायता लें।", "care_urgent": "इसके लिए तुरंत पशु चिकित्सक की सहायता आवश्यक हो सकती है।", "care_wound": "घाव साफ रखें और पशु को उस जगह पर दोबारा चोट लगने से बचाएँ।", "care_ticks": "ज़रूरत पड़ने पर प्रभावित पशु को अलग रखें और सुरक्षित परजीवी नियंत्रण के लिए पशु चिकित्सक से पूछें।", "care_vet": "पशु चिकित्सक से जाँच कराने की दृढ़ सलाह दी जाती है।", "care_no_medicine": "पशु चिकित्सक की सलाह के बिना दवा न दें।",
        "open_module": "{title} खोलें", "appointment_success": "अपॉइंटमेंट अनुरोध जमा किया गया।", "no_appointments": "कोई अपॉइंटमेंट उपलब्ध नहीं है।",
        "status_label": "स्थिति", "status_pending": "लंबित", "status_approved": "स्वीकृत", "status_rejected": "अस्वीकृत",
        "lab_result": "जाँच का परिणाम", "medicine": "पशु चिकित्सा निर्देश", "follow_up": "फॉलो-अप आवश्यक", "notes": "टिप्पणियाँ",
        "app_name": "पशुरक्षा",
        "subtitle": "पशुधन स्वास्थ्य और सुरक्षा",
        "landing_title": "पशुओं की रक्षा। समुदायों की रक्षा।",
        "welcome": "स्वागत",
        "full_name": "पूरा नाम",
        "mobile": "फ़ोन नंबर",
        "continue": "पोर्टल खोलें",
        "profile_required": "आगे बढ़ने के लिए अपना नाम और फ़ोन नंबर दर्ज करें।",
        "choose_portal": "अपना पोर्टल चुनें",
        "farmer": "किसान",
        "veterinarian": "पशु चिकित्सक",
        "government": "सरकार",
        "farmer_portal": "किसान पोर्टल",
        "veterinarian_portal": "पशु चिकित्सक पोर्टल",
        "government_portal": "सरकारी पोर्टल",
        "farmer_desc": "बीमार पशुओं की रिपोर्ट करें और गांव का स्वास्थ्य देखें",
        "veterinarian_desc": "मामलों का प्रबंधन करें और स्वास्थ्य अलर्ट पर प्रतिक्रिया दें",
        "government_desc": "गाँव, जोखिम और पशुधन स्वास्थ्य जानकारी देखें",
        "back_to_profile": "प्रोफ़ाइल पर वापस",
        "read_aloud": "पढ़कर सुनाएँ",
        "select_all": "सभी चुनें",
        "clear_selection": "साफ़ करें",
        "animal_health_report": "पशु स्वास्थ्य रिपोर्ट",
        "village_health": "गाँव का स्वास्थ्य",
        "health_alerts": "स्वास्थ्य अलर्ट",
        "previous_reports": "पिछली रिपोर्टें",
        "report_another": "अतिरिक्त पशु रिपोर्ट करें",
        "submit_report": "स्वास्थ्य रिपोर्ट जमा करें",
        "submit_success": "स्वास्थ्य रिपोर्ट सफलतापूर्वक जमा की गई।",
        "symptoms": "लक्षण",
        "days_sick": "बीमार दिनों की संख्या",
        "village": "गाँव",
        "risk_score": "जोखिम स्कोर",
        "health_condition": "स्वास्थ्य स्थिति",
        "health_advice": "स्वास्थ्य सलाह",
        "possible_conditions": "संभावित स्थितियाँ",
        "disease_risk_prediction": "रोग जोखिम भविष्यवाणी",
        "reported_animal": "रिपोर्ट किया गया पशु",
        "detected_symptoms": "पाए गए लक्षण",
        "time": "समय",
        "risk_level": "जोखिम स्तर",
        "disclaimer": "यह एक लक्षण-आधारित स्वास्थ्य जोखिम आकलन है और पेशेवर पशु चिकित्सा निदान नहीं है।",
        "total_reports": "कुल रिपोर्ट",
        "high_risk_cases": "उच्च जोखिम मामले",
        "medium_risk_cases": "मध्यम जोखिम मामले",
        "low_risk_cases": "कम जोखिम मामले",
        "total_villages": "कुल गाँव",
        "recent_reports": "हाल की रिपोर्टें",
        "village_summary": "गाँव स्वास्थ्य सारांश",
        "validation_missing_village": "कृपया गाँव का नाम दर्ज करें।",
        "validation_missing_symptoms": "कृपया कम से कम एक लक्षण चुनें।",
        "validation_missing_animals": "कृपया कम से कम एक पशु चुनें।",
        "village_risk": "गाँव जोखिम",
        "alert_summary": "स्वास्थ्य अलर्ट",
        "response_note": "प्रतिक्रिया नोट",
        "save_response": "प्रतिक्रिया सेव करें",
        "completed": "समीक्षा पूर्ण",
        "low_risk": "कम जोखिम",
        "medium_risk": "मध्यम जोखिम",
        "high_risk": "उच्च जोखिम",
        "no_reports": "कोई रिपोर्ट उपलब्ध नहीं है।",
        "no_alerts": "कोई स्वास्थ्य अलर्ट नहीं।",
        "animal_selection": "पशु चयन",
    },
    "Kannada": {
        "yes": "ಹೌದು", "no": "ಇಲ್ಲ",
        "respiratory_warning": "ಉಸಿರಾಟದ ಕಾಯಿಲೆಯ ಎಚ್ಚರಿಕೆ", "digestive_warning": "ಜೀರ್ಣಕ್ರಿಯೆ / ನಿರ್ಜಲೀಕರಣದ ಎಚ್ಚರಿಕೆ", "skin_warning": "ಚರ್ಮ ಅಥವಾ ಪರೋಪಜೀವಿ ಎಚ್ಚರಿಕೆ", "injury_warning": "ಗಾಯ ಅಥವಾ ಉರಿಯೂತದ ಎಚ್ಚರಿಕೆ", "general_warning": "ಸಾಮಾನ್ಯ ಕಾಯಿಲೆ / ಪೋಷಣೆಯ ಎಚ್ಚರಿಕೆ", "milk_warning": "ಹಾಲು ಉತ್ಪಾದನೆ / ಕೆಚ್ಚಲಿನ ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆ", "neurological_warning": "ನರವ್ಯವಸ್ಥೆಯ ಎಚ್ಚರಿಕೆ", "no_pattern": "ನಿರ್ದಿಷ್ಟ ಸ್ಥಿತಿಯ ಲಕ್ಷಣ ಪತ್ತೆಯಾಗಿಲ್ಲ",
        "care_clean_water": "ಶುದ್ಧ ಕುಡಿಯುವ ನೀರು ನೀಡಿ, ಪಶುವನ್ನು ಸ್ವಚ್ಛ, ಆರಾಮದಾಯಕ ಮತ್ತು ನೆರಳಿನ ಸ್ಥಳದಲ್ಲಿಡಿ.", "care_dehydration": "ನಿರ್ಜಲೀಕರಣ ಗಮನಿಸಿ; ಲಕ್ಷಣಗಳು ಮುಂದುವರಿದರೆ ಅಥವಾ ಹದಗೆಟ್ಟರೆ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.", "care_breathing": "ಉಸಿರಾಟದ ತೊಂದರೆ ತುರ್ತು ಪರಿಸ್ಥಿತಿಯಾಗಬಹುದು. ತಕ್ಷಣ ಪಶುವೈದ್ಯಕೀಯ ನೆರವು ಪಡೆಯಿರಿ.", "care_urgent": "ತುರ್ತು ಪಶುವೈದ್ಯಕೀಯ ಆರೈಕೆ ಅಗತ್ಯವಾಗಬಹುದು.", "care_wound": "ಗಾಯಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ ಮತ್ತು ಪಶು ಮತ್ತೆ ಗಾಯಗೊಳ್ಳದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.", "care_ticks": "ಅಗತ್ಯವಿದ್ದಲ್ಲಿ ಬಾಧಿತ ಪಶುವನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ; ಸುರಕ್ಷಿತ ಪರೋಪಜೀವಿ ನಿಯಂತ್ರಣಕ್ಕೆ ಪಶುವೈದ್ಯರನ್ನು ಕೇಳಿ.", "care_vet": "ಪಶುವೈದ್ಯಕೀಯ ಪರೀಕ್ಷೆಯನ್ನು ಬಲವಾಗಿ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ.", "care_no_medicine": "ಪಶುವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಔಷಧಿ ನೀಡಬೇಡಿ.",
        "open_module": "{title} ತೆರೆಯಿರಿ", "appointment_success": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿ ಸಲ್ಲಿಸಲಾಗಿದೆ.", "no_appointments": "ಯಾವುದೇ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳಿಲ್ಲ.",
        "status_label": "ಸ್ಥಿತಿ", "status_pending": "ಬಾಕಿಯಿದೆ", "status_approved": "ಅನುಮೋದಿಸಲಾಗಿದೆ", "status_rejected": "ತಿರಸ್ಕರಿಸಲಾಗಿದೆ",
        "lab_result": "ಪರೀಕ್ಷೆಯ ಫಲಿತಾಂಶ", "medicine": "ಪಶುವೈದ್ಯಕೀಯ ಸೂಚನೆಗಳು", "follow_up": "ಮರುಪರಿಶೀಲನೆ ಅಗತ್ಯ", "notes": "ಟಿಪ್ಪಣಿಗಳು",
        "app_name": "ಪಶುರಕ್ಷಾ",
        "subtitle": "ಪಶು ಆರೋಗ್ಯ ಮತ್ತು ಸುರಕ್ಷತೆ",
        "landing_title": "ಪಶುಗಳನ್ನು ರಕ್ಷಿಸಿ. ಸಮುದಾಯಗಳನ್ನು ರಕ್ಷಿಸಿ.",
        "welcome": "ಸ್ವಾಗತ",
        "full_name": "ಪೂರ್ಣ ಹೆಸರು",
        "mobile": "ಫೋನ್ ಸಂಖ್ಯೆ",
        "continue": "ಪೋರ್ಟಲ್ ತೆರೆಯಿರಿ",
        "profile_required": "ಮುಂದುವರಿಸಲು ನಿಮ್ಮ ಹೆಸರು ಮತ್ತು ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "choose_portal": "ನಿಮ್ಮ ಪೋರ್ಟಲ್ ಆಯ್ಕೆಮಾಡಿ",
        "farmer": "ರೈತ",
        "veterinarian": "ಪಶುವೈದ್ಯ",
        "government": "ಸರ್ಕಾರ",
        "farmer_portal": "ರೈತ ಪೋರ್ಟಲ್",
        "veterinarian_portal": "ಪಶುವೈದ್ಯ ಪೋರ್ಟಲ್",
        "government_portal": "ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್",
        "farmer_desc": "ಅಸ್ವಸ್ಥ ಪಶುಗಳನ್ನು ವರದಿ ಮಾಡಿ ಮತ್ತು ಗ್ರಾಮ ಆರೋಗ್ಯವನ್ನು ಪರಿಶೀಲಿಸಿ",
        "veterinarian_desc": "ಕೇಸ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ ಮತ್ತು ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆಗಳಿಗೆ ಉತ್ತರಿಸಿ",
        "government_desc": "ಗ್ರಾಮಗಳು, ಅಪಾಯಗಳು ಮತ್ತು ಪಶು ಆರೋಗ್ಯ ಮಾಹಿತಿಯನ್ನು ಗಮನಿಸಿ",
        "back_to_profile": "ಪ್ರೊಫೈಲ್‌ಗೆ ಹಿಂದಿರುಗಿ",
        "read_aloud": "ಓದಿಸಿ",
        "select_all": "ಎಲ್ಲವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "clear_selection": "ಸ್ಪಷ್ಟ ಮಾಡಿ",
        "animal_health_report": "ಪಶು ಆರೋಗ್ಯ ವರದಿ",
        "village_health": "ಗ್ರಾಮ ಆರೋಗ್ಯ",
        "health_alerts": "ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆಗಳು",
        "previous_reports": "ಹಿಂದಿನ ವರದಿಗಳು",
        "report_another": "ಮತ್ತೊಂದು ಪಶುವನ್ನು ವರದಿ ಮಾಡಿ",
        "submit_report": "ಆರೋಗ್ಯ ವರದಿ ಸಲ್ಲಿಸಿ",
        "submit_success": "ಆರೋಗ್ಯ ವರದಿ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ.",
        "symptoms": "ಲಕ್ಷಣಗಳು",
        "days_sick": "ಅಸ್ವಸ್ಥವಾಗಿದ್ದ ದಿನಗಳು",
        "village": "ಗ್ರಾಮ",
        "risk_score": "ಅಪಾಯ ಅಂಕ",
        "health_condition": "ಆರೋಗ್ಯ ಸ್ಥಿತಿ",
        "health_advice": "ಆರೋಗ್ಯ ಸಲಹೆ",
        "possible_conditions": "ಸಂಭಾವ್ಯ ಪರಿಸ್ಥಿತಿಗಳು",
        "disease_risk_prediction": "ರೋಗ ಅಪಾಯ ಮುನ್ಸೂಚನೆ",
        "reported_animal": "ವರದಿ ಮಾಡಿದ ಪಶು",
        "detected_symptoms": "ಪತ್ತೆಯಾದ ಲಕ್ಷಣಗಳು",
        "time": "ಸಮಯ",
        "risk_level": "ಅಪಾಯ ಮಟ್ಟ",
        "disclaimer": "ಇದು ಒಂದು ಲಕ್ಷಣ-ಆಧಾರಿತ ಆರೋಗ್ಯ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ ಮತ್ತು ವೃತ್ತಿಪರ ಪಶು ವೈದ್ಯರ ರೋಗನಿರ್ಣಯವಲ್ಲ.",
        "total_reports": "ಒಟ್ಟು ವರದಿಗಳು",
        "high_risk_cases": "ಹೆಚ್ಚಿನ ಅಪಾಯದ ಪ್ರಕರಣಗಳು",
        "medium_risk_cases": "ಮಧ್ಯಮ ಅಪಾಯದ ಪ್ರಕರಣಗಳು",
        "low_risk_cases": "ಕಡಿಮೆ ಅಪಾಯದ ಪ್ರಕರಣಗಳು",
        "total_villages": "ಒಟ್ಟು ಗ್ರಾಮಗಳು",
        "recent_reports": "ಇತ್ತೀಚಿನ ವರದಿಗಳು",
        "village_summary": "ಗ್ರಾಮ ಆರೋಗ್ಯ ಸಾರಾಂಶ",
        "validation_missing_village": "ದಯವಿಟ್ಟು ಗ್ರಾಮದ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "validation_missing_symptoms": "ದಯವಿಟ್ಟು ಕನಿಷ್ಠ ಒಂದು ಲಕ್ಷಣ ಆಯ್ಕೆಮಾಡಿ.",
        "validation_missing_animals": "ದಯವಿಟ್ಟು ಕನಿಷ್ಠ ಒಂದು ಪಶುವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "village_risk": "ಗ್ರಾಮ ಅಪಾಯ",
        "alert_summary": "ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆಗಳು",
        "response_note": "ಪ್ರತಿಕ್ರಿಯೆ ಟಿಪ್ಪಣಿ",
        "save_response": "ಪ್ರತಿಕ್ರಿಯೆ ಉಳಿಸಿ",
        "completed": "ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
        "low_risk": "ಕಡಿಮೆ ಅಪಾಯ",
        "medium_risk": "ಮಧ್ಯಮ ಅಪಾಯ",
        "high_risk": "ಹೆಚ್ಚಿನ ಅಪಾಯ",
        "no_reports": "ಯಾವುದೇ ವರದಿಗಳಿಲ್ಲ.",
        "no_alerts": "ಯಾವುದೇ ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆಗಳಿಲ್ಲ.",
        "animal_selection": "ಪಶು ಆಯ್ಕೆ",
    },
    "Marathi": {
        "yes": "होय", "no": "नाही",
        "respiratory_warning": "श्वसन आजाराचा इशारा", "digestive_warning": "पचन / निर्जलीकरणाचा इशारा", "skin_warning": "त्वचा किंवा परजीवी इशारा", "injury_warning": "इजा किंवा सूज इशारा", "general_warning": "सामान्य आजार / पोषण इशारा", "milk_warning": "दूध उत्पादन / कास आरोग्य इशारा", "neurological_warning": "न्यूरोलॉजिकल इशारा", "no_pattern": "विशिष्ट स्थितीचा नमुना आढळला नाही",
        "care_clean_water": "स्वच्छ पिण्याचे पाणी द्या आणि पशूला स्वच्छ, आरामदायी व सावलीच्या जागी ठेवा.", "care_dehydration": "निर्जलीकरणावर लक्ष ठेवा; लक्षणे सुरू राहिल्यास किंवा वाढल्यास पशुवैद्याशी संपर्क साधा.", "care_breathing": "श्वास घेण्यास त्रास तातडीची स्थिती असू शकते. लगेच पशुवैद्यकीय मदत घ्या.", "care_urgent": "तातडीची पशुवैद्यकीय मदत आवश्यक असू शकते.", "care_wound": "जखमा स्वच्छ ठेवा आणि पशूला त्या भागाला पुन्हा इजा होण्यापासून वाचवा.", "care_ticks": "गरज असल्यास बाधित पशूला वेगळे ठेवा आणि सुरक्षित परजीवी नियंत्रणासाठी पशुवैद्याचा सल्ला घ्या.", "care_vet": "पशुवैद्यकीय तपासणीची जोरदार शिफारस केली जाते.", "care_no_medicine": "पशुवैद्यकीय सल्ल्याशिवाय औषध देऊ नका.",
        "open_module": "{title} उघडा", "appointment_success": "भेटीची विनंती सादर केली.", "no_appointments": "भेटी उपलब्ध नाहीत.",
        "status_label": "स्थिती", "status_pending": "प्रलंबित", "status_approved": "मंजूर", "status_rejected": "नामंजूर",
        "lab_result": "तपासणीचा निकाल", "medicine": "पशुवैद्यकीय सूचना", "follow_up": "पुढील तपासणी आवश्यक", "notes": "नोंदी",
        "app_name": "पशुरक्षा",
        "subtitle": "पशुधन आरोग्य आणि सुरक्षा",
        "landing_title": "पशूंची संरक्षण. समुदायांची संरक्षण.",
        "welcome": "स्वागत",
        "full_name": "पूर्ण नाव",
        "mobile": "फोन नंबर",
        "continue": "पोर्टल उघडा",
        "profile_required": "पुढे जाण्यासाठी तुमचे नाव आणि फोन नंबर भरा.",
        "choose_portal": "आपले पोर्टल निवडा",
        "farmer": "शेतकरी",
        "veterinarian": "पशुवैद्य",
        "government": "सरकार",
        "farmer_portal": "शेतकरी पोर्टल",
        "veterinarian_portal": "पशुवैद्य पोर्टल",
        "government_portal": "सरकारी पोर्टल",
        "farmer_desc": "आजारी पशूंची नोंद करा आणि गावातील आरोग्य तपासा",
        "veterinarian_desc": "केसेस व्यवस्थापित करा आणि आरोग्य अलर्टना प्रतिसाद द्या",
        "government_desc": "गाव, जोखीम आणि पशुधन आरोग्य माहिती पाहा",
        "back_to_profile": "प्रोफाइलवर परत",
        "read_aloud": "वाचून ऐका",
        "select_all": "सर्व निवडा",
        "clear_selection": "साफ करा",
        "animal_health_report": "पशू आरोग्य अहवाल",
        "village_health": "गाव आरोग्य",
        "health_alerts": "आरोग्य अलर्ट",
        "previous_reports": "मागील अहवाल",
        "report_another": "अजून एक प्राणी नोंदवा",
        "submit_report": "आरोग्य अहवाल सबमिट करा",
        "submit_success": "आरोग्य अहवाल यशस्वीरित्या सबमिट झाला.",
        "symptoms": "लक्षणे",
        "days_sick": "आजारी राहिलेल्या दिवसांची संख्या",
        "village": "गाव",
        "risk_score": "जोखीम स्कोर",
        "health_condition": "आरोग्य स्थिती",
        "health_advice": "आरोग्य सल्ला",
        "possible_conditions": "संभाव्य परिस्थिती",
        "disease_risk_prediction": "रोग जोखीम अंदाज",
        "reported_animal": "नोंदलेले प्राणी",
        "detected_symptoms": "आढळलेले लक्षण",
        "time": "वेळ",
        "risk_level": "जोखीम स्तर",
        "disclaimer": "हा लक्षण-आधारित आरोग्य जोखीम मूल्यांकन आहे आणि व्यावसायिक पशुवैद्यकीय निदान नाही.",
        "total_reports": "एकूण अहवाल",
        "high_risk_cases": "उच्च जोखीम प्रकरणे",
        "medium_risk_cases": "मध्यम जोखीम प्रकरणे",
        "low_risk_cases": "कमी जोखीम प्रकरणे",
        "total_villages": "एकूण गाव",
        "recent_reports": "अलीकडील अहवाल",
        "village_summary": "गाव आरोग्य सारांश",
        "validation_missing_village": "कृपया गावाचे नाव भरा.",
        "validation_missing_symptoms": "कृपया कमीत कमी एक लक्षण निवडा.",
        "validation_missing_animals": "कृपया कमीत कमी एक प्राणी निवडा.",
        "village_risk": "गाव जोखीम",
        "alert_summary": "आरोग्य अलर्ट",
        "response_note": "प्रतिसाद नोट",
        "save_response": "प्रतिसाद सेव करा",
        "completed": "तपासणी पूर्ण",
        "low_risk": "कमी जोखीम",
        "medium_risk": "मध्यम जोखीम",
        "high_risk": "उच्च जोखीम",
        "no_reports": "कोणतेही अहवाल उपलब्ध नाहीत.",
        "no_alerts": "कोणतेही आरोग्य अलर्ट नाहीत.",
        "animal_selection": "प्राणी निवड",
    },
    "Telugu": {
        "yes": "అవును", "no": "కాదు",
        "respiratory_warning": "శ్వాసకోశ వ్యాధి హెచ్చరిక", "digestive_warning": "జీర్ణక్రియ / డీహైడ్రేషన్ హెచ్చరిక", "skin_warning": "చర్మం లేదా పరాన్నజీవుల హెచ్చరిక", "injury_warning": "గాయం లేదా వాపు హెచ్చరిక", "general_warning": "సాధారణ అనారోగ్యం / పోషణ హెచ్చరిక", "milk_warning": "పాల ఉత్పత్తి / పొదుగు ఆరోగ్య హెచ్చరిక", "neurological_warning": "నరాల సంబంధిత హెచ్చరిక", "no_pattern": "నిర్దిష్ట పరిస్థితి నమూనా గుర్తించబడలేదు",
        "care_clean_water": "శుభ్రమైన తాగునీరు ఇవ్వండి; పశువును శుభ్రమైన, సౌకర్యవంతమైన, నీడగల ప్రదేశంలో ఉంచండి.", "care_dehydration": "డీహైడ్రేషన్‌ను గమనించండి; లక్షణాలు కొనసాగినా లేదా తీవ్రమైనా పశువైద్యుడిని సంప్రదించండి.", "care_breathing": "శ్వాస తీసుకోవడంలో ఇబ్బంది అత్యవసర పరిస్థితి కావచ్చు. వెంటనే పశువైద్య సహాయం పొందండి.", "care_urgent": "అత్యవసర పశువైద్య శ్రద్ధ అవసరం కావచ్చు.", "care_wound": "గాయాలను శుభ్రంగా ఉంచి, ఆ ప్రాంతానికి మళ్లీ గాయం కాకుండా చూడండి.", "care_ticks": "అవసరమైతే ప్రభావిత పశువును వేరుగా ఉంచి, సురక్షిత పరాన్నజీవి నియంత్రణ గురించి పశువైద్యుడిని అడగండి.", "care_vet": "పశువైద్య పరీక్ష చేయించుకోవాలని గట్టిగా సిఫార్సు చేస్తున్నాము.", "care_no_medicine": "పశువైద్యుడి సలహా లేకుండా మందులు ఇవ్వవద్దు.",
        "open_module": "{title} తెరవండి", "appointment_success": "అపాయింట్‌మెంట్ అభ్యర్థన సమర్పించబడింది.", "no_appointments": "అపాయింట్‌మెంట్‌లు లేవు.",
        "status_label": "స్థితి", "status_pending": "పెండింగ్‌లో ఉంది", "status_approved": "ఆమోదించబడింది", "status_rejected": "తిరస్కరించబడింది",
        "lab_result": "పరీక్ష ఫలితం", "medicine": "పశువైద్య సూచనలు", "follow_up": "తదుపరి పరీక్ష అవసరం", "notes": "గమనికలు",
        "app_name": "పశురక్షా",
        "subtitle": "పశు ఆరోగ్య మరియు భద్రత",
        "landing_title": "పశువులను రక్షించండి. కమ్యూనిటీలను రక్షించండి.",
        "welcome": "స్వాగతం",
        "full_name": "పూర్తి పేరు",
        "mobile": "ఫోన్ నంబర్",
        "continue": "పోర్టల్ తెరవండి",
        "profile_required": "కొనసాగించడానికి మీ పేరు మరియు ఫోన్ నంబర్ నమోదు చేయండి.",
        "choose_portal": "మీ పోర్టల్‌ను ఎంచుకోండి",
        "farmer": "రైతు",
        "veterinarian": "పశువైద్యుడు",
        "government": "సర్కారు",
        "farmer_portal": "రైతు పోర్టల్",
        "veterinarian_portal": "పశువైద్య పోర్టల్",
        "government_portal": "సర్కారీ పోర్టల్",
        "farmer_desc": "అస్వస్థ పశువులను నివేదించి గ్రామ ఆరోగ్యాన్ని పరిశీలించండి",
        "veterinarian_desc": "కేసులను నిర్వహించి ఆరోగ్య అలర్ట్లకు స్పందించండి",
        "government_desc": "గ్రామాలు, ప్రమాదాలు మరియు పశు ఆరోగ్య సమాచారాన్ని monitor చేయండి",
        "back_to_profile": "ప్రొఫైల్‌కి తిరిగి వెళ్లండి",
        "read_aloud": "చదివి వినిపించండి",
        "select_all": "అన్నింటినీ ఎంచుకోండి",
        "clear_selection": "స్పష్టం చేయండి",
        "animal_health_report": "పశు ఆరోగ్య నివేదిక",
        "village_health": "గ్రామ ఆరోగ్యము",
        "health_alerts": "ఆరోగ్య అలర్ట్స్",
        "previous_reports": "ఇప్పటికే పంపిన నివేదికలు",
        "report_another": "మరో జంతువును నివేదించండి",
        "submit_report": "ఆరోగ్య నివేదిక సమర్పించండి",
        "submit_success": "ఆరోగ్య నివేదిక విజయవంతంగా సమర్పించబడింది.",
        "symptoms": "లక్షణాలు",
        "days_sick": "అస్వస్థత గడిచిన రోజులు",
        "village": "గ్రామం",
        "risk_score": "రిస్క్ స్కోర్",
        "health_condition": "ఆరోగ్య స్థితి",
        "health_advice": "ఆరోగ్య సలహా",
        "possible_conditions": "సాధ్యమయ్యే పరిస్థితులు",
        "disease_risk_prediction": "వ్యాధి ప్రమాద అంచనా",
        "reported_animal": "నివేదించిన జంతువు",
        "detected_symptoms": "పేలిన లక్షణాలు",
        "time": "సమయం",
        "risk_level": "రిస్క్ లెవెల్",
        "disclaimer": "ఇది లక్షణ-ఆధారిత ఆరోగ్య ప్రమాద అంచనా మాత్రమే, వృత్తిపరమైన పశువైద్య నిర్ధారణ కాదు.",
        "total_reports": "మొత్తం నివేదికలు",
        "high_risk_cases": "అత్యంత ప్రమాదకర కేసులు",
        "medium_risk_cases": "మధ్యస్థ ప్రమాద కేసులు",
        "low_risk_cases": "తక్కువ ప్రమాద కేసులు",
        "total_villages": "మొత్తం గ్రామాలు",
        "recent_reports": "ఇటీవలి నివేదికలు",
        "village_summary": "గ్రామ ఆరోగ్య సంక్షిప్తం",
        "validation_missing_village": "దయచేసి గ్రామం పేరు నమోదు చేయండి.",
        "validation_missing_symptoms": "దయచేసి కనీసం ఒక లక్షణాన్ని ఎంచుకోండి.",
        "validation_missing_animals": "దయచేసి కనీసం ఒక జంతువును ఎంచుకోండి.",
        "village_risk": "గ్రామ ప్రమాదం",
        "alert_summary": "ఆరోగ్య అలర్ట్స్",
        "response_note": "స్పందన గమనిక",
        "save_response": "స్పందనను సేవ్ చేయండి",
        "completed": "సమీక్షించబడింది",
        "low_risk": "తక్కువ ప్రమాదం",
        "medium_risk": "మధ్యస్థ ప్రమాదం",
        "high_risk": "అత్యంత ప్రమాదం",
        "no_reports": "నివేదికలు లేవు.",
        "no_alerts": "ఆరోగ్య అలర్ట్లు లేవు.",
        "animal_selection": "జంతువు ఎంపిక",
    },
    "Tamil": {
        "yes": "ஆம்", "no": "இல்லை",
        "respiratory_warning": "சுவாச நோய் எச்சரிக்கை", "digestive_warning": "செரிமானம் / நீரிழப்பு எச்சரிக்கை", "skin_warning": "தோல் அல்லது ஒட்டுண்ணி எச்சரிக்கை", "injury_warning": "காயம் அல்லது வீக்கம் எச்சரிக்கை", "general_warning": "பொதுவான நோய் / ஊட்டச்சத்து எச்சரிக்கை", "milk_warning": "பால் உற்பத்தி / மடி ஆரோக்கிய எச்சரிக்கை", "neurological_warning": "நரம்பியல் எச்சரிக்கை", "no_pattern": "குறிப்பிட்ட உடல்நிலை முறை எதுவும் கண்டறியப்படவில்லை",
        "care_clean_water": "சுத்தமான குடிநீர் வழங்கி, கால்நடையை சுத்தமான, வசதியான நிழலான இடத்தில் வைக்கவும்.", "care_dehydration": "நீரிழப்பைக் கவனிக்கவும்; அறிகுறிகள் தொடர்ந்தால் அல்லது மோசமடைந்தால் கால்நடை மருத்துவரை அணுகவும்.", "care_breathing": "சுவாசிப்பதில் சிரமம் அவசர நிலையாக இருக்கலாம். உடனடியாக கால்நடை மருத்துவ உதவியைப் பெறவும்.", "care_urgent": "அவசர கால்நடை மருத்துவ கவனம் தேவைப்படலாம்.", "care_wound": "காயங்களை சுத்தமாக வைத்து, அந்த இடத்தில் மீண்டும் காயம் ஏற்படாமல் தடுக்கவும்.", "care_ticks": "தேவையானபோது பாதிக்கப்பட்ட கால்நடையைத் தனியாக வைத்து, பாதுகாப்பான ஒட்டுண்ணி கட்டுப்பாட்டை மருத்துவரிடம் கேட்கவும்.", "care_vet": "கால்நடை மருத்துவர் பரிசோதனை வலுவாக பரிந்துரைக்கப்படுகிறது.", "care_no_medicine": "கால்நடை மருத்துவர் ஆலோசனையின்றி மருந்து கொடுக்க வேண்டாம்.",
        "open_module": "{title} திறக்கவும்", "appointment_success": "சந்திப்பு கோரிக்கை சமர்ப்பிக்கப்பட்டது.", "no_appointments": "சந்திப்புகள் இல்லை.",
        "status_label": "நிலை", "status_pending": "நிலுவையில்", "status_approved": "அங்கீகரிக்கப்பட்டது", "status_rejected": "நிராகரிக்கப்பட்டது",
        "lab_result": "பரிசோதனை முடிவு", "medicine": "கால்நடை மருத்துவ வழிமுறைகள்", "follow_up": "மீண்டும் பரிசோதனை தேவை", "notes": "குறிப்புகள்",
        "app_name": "பசுரக்ஷா",
        "subtitle": "கால்நடை ஆரோக்கியம் மற்றும் பாதுகாப்பு",
        "landing_title": "கால்நடைகளைப் பாதுகாத்து. சமூகங்களைப் பாதுகாத்து.",
        "welcome": "வரவேற்கிறோம்",
        "full_name": "முழுப் பெயர்",
        "mobile": "தொலைபேசி எண்",
        "continue": "போர்டலைத் திறக்கவும்",
        "profile_required": "தொடர உங்கள் பெயர் மற்றும் தொலைபேசி எண்ணை உள்ளிடவும்.",
        "choose_portal": "உங்கள் போர்டலைத் தேர்ந்தெடுக்கவும்",
        "farmer": "விவசாயி",
        "veterinarian": "கால்நடை மருத்துவர்",
        "government": "அரசு",
        "farmer_portal": "விவசாயி போர்டல்",
        "veterinarian_portal": "கால்நடை மருத்துவர் போர்டல்",
        "government_portal": "அரசு போர்டல்",
        "farmer_desc": "நோயுற்ற கால்நடைகளை அறிவித்து கிராம ஆரோக்கியத்தைப் பார்க்கவும்",
        "veterinarian_desc": "வழக்குகளை நிர்வகித்து ஆரோக்கிய எச்சரிக்கைகளுக்கு பதிலளிக்கவும்",
        "government_desc": "கிராமங்கள், ஆபத்துகள் மற்றும் கால்நடை ஆரோக்கியத் தகவல்களை கண்காணிக்கவும்",
        "back_to_profile": "சுயவிவரத்திற்கு திரும்பு",
        "read_aloud": "படித்து கேளுங்கள்",
        "select_all": "அனைத்தையும் தேர்ந்தெடுக்கவும்",
        "clear_selection": "சுத்தம்",
        "animal_health_report": "கால்நடை ஆரோக்கிய அறிக்கை",
        "village_health": "கிராம ஆரோக்கியம்",
        "health_alerts": "ஆரோக்கிய எச்சரிக்கைகள்",
        "previous_reports": "முந்தைய அறிக்கைகள்",
        "report_another": "மற்றொரு விலங்கை அறிக்கை செய்யுங்கள்",
        "submit_report": "ஆரோக்கிய அறிக்கையை சமர்ப்பிக்கவும்",
        "submit_success": "ஆரோக்கிய அறிக்கை வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது.",
        "symptoms": "அறிகுறிகள்",
        "days_sick": "நோயுற்றிருந்த நாட்கள்",
        "village": "கிராமம்",
        "risk_score": "ஆபத்து மதிப்பெண்",
        "health_condition": "ஆரோக்கிய நிலை",
        "health_advice": "ஆரோக்கிய ஆலோசனை",
        "possible_conditions": "சாத்தியமான நிலைகள்",
        "disease_risk_prediction": "நோய் ஆபத்து கணிப்பு",
        "reported_animal": "அறிக்கையிடப்பட்ட விலங்கு",
        "detected_symptoms": "கண்டறியப்பட்ட அறிகுறிகள்",
        "time": "நேரம்",
        "risk_level": "ஆபத்து நிலை",
        "disclaimer": "இது அறிகுறி அடிப்படையிலான ஆரோக்கிய ஆபத்து மதிப்பீடு மட்டுமே; தொழில்முறை கால்நடை நோயறிதல் அல்ல.",
        "total_reports": "மொத்த அறிக்கைகள்",
        "high_risk_cases": "உயர் ஆபத்து நிகழ்வுகள்",
        "medium_risk_cases": "மத்திய ஆபத்து நிகழ்வுகள்",
        "low_risk_cases": "குறைந்த ஆபத்து நிகழ்வுகள்",
        "total_villages": "மொத்த கிராமங்கள்",
        "recent_reports": "சமீப அறிக்கைகள்",
        "village_summary": "கிராம ஆரோக்கிய சுருக்கம்",
        "validation_missing_village": "கிராமத்தின் பெயரை உள்ளிடவும்.",
        "validation_missing_symptoms": "குறைந்தபட்சம் ஒரு அறிகுறியை தேர்ந்தெடுக்கவும்.",
        "validation_missing_animals": "குறைந்தபட்சம் ஒரு விலங்கை தேர்ந்தெடுக்கவும்.",
        "village_risk": "கிராம ஆபத்து",
        "alert_summary": "ஆரோக்கிய எச்சரிக்கைகள்",
        "response_note": "பதில் குறிப்புகள்",
        "save_response": "பதிலைச் சேமி",
        "completed": "மதிப்பாய்வு முடிந்தது",
        "low_risk": "குறைந்த ஆபத்து",
        "medium_risk": "மத்திய ஆபத்து",
        "high_risk": "உயர் ஆபத்து",
        "no_reports": "அறிக்கைகள் எதுவும் இல்லை.",
        "no_alerts": "ஆரோக்கிய எச்சரிக்கைகள் இல்லை.",
        "animal_selection": "விலங்கு தேர்வு",
    },
}

TRANSLATION_EXTRAS = {
    "English": {
        "language_label": "Language", "profile_heading": "Profile", "profile_description": "Enter your details to open your portal.",
        "hero_eyebrow": "Smart Livestock Health Monitoring", "back_modules": "Back to modules", "demo_data": "Demo Data",
        "demo_profiles": "Demo Profiles", "demo_credentials": "Demo profile credentials", "use_demo": "Use Demo",
        "demo_farmer": "Farmer Demo", "demo_veterinary": "Veterinary Demo", "demo_government": "Government Demo",
        "demo_farmer_name": "Demo Farmer", "demo_veterinary_name": "Demo Veterinary", "demo_government_name": "Demo Government",
        "animal_health": "Animal Health Check", "animal_health_desc": "Check livestock health risk using reported symptoms.",
        "appointments_module": "Appointments", "appointments_desc": "Book and track veterinary appointments.",
        "reports_module": "My Reports", "reports_desc": "View all animal health reports you submitted.",
        "notifications_module": "Notifications", "notifications_desc": "View important health and appointment updates.",
        "animal_care_module": "Animal Care", "animal_care_desc": "Learn about common livestock health problems and care.",
        "animal_reports_module": "Animal Reports", "animal_reports_desc": "Review livestock health reports submitted by farmers.",
        "appointment_requests_module": "Appointment Requests", "appointment_requests_desc": "Review and manage farmer veterinary requests.",
        "laboratory_module": "Laboratory", "laboratory_desc": "Add veterinary examination and laboratory results.",
        "village_risk_module": "Village Risk", "village_risk_desc": "Monitor animal health risk across villages.",
        "risk_management_module": "Risk Management", "risk_management_desc": "Monitor risk levels and plan interventions.",
        "role_caption": "{name} · {role} Portal", "animal_type": "Animal type", "appointment_date": "Appointment date",
        "appointment_time": "Appointment time", "reason": "Reason for appointment", "request_appointment": "Request appointment",
        "enter_reason": "Enter a reason for the appointment.", "no_appointment_requests": "No appointment requests yet.",
        "no_laboratory_records": "No laboratory records yet.", "care_guidance": "Provide clean water and a clean, shaded resting area. Contact a veterinarian for serious, persistent, or worsening symptoms. Do not give prescription medicines without veterinary guidance.",
        "risk_critical": "Critical", "risk_high_concern": "High Concern", "risk_moderate_concern": "Moderate Concern", "risk_mild_concern": "Mild Concern",
    },
    "Hindi": {
        "language_label": "भाषा", "profile_heading": "प्रोफ़ाइल", "profile_description": "अपना पोर्टल खोलने के लिए अपना विवरण दर्ज करें।",
        "hero_eyebrow": "स्मार्ट पशुधन स्वास्थ्य निगरानी", "back_modules": "मॉड्यूल पर वापस जाएँ", "demo_data": "डेमो डेटा",
        "demo_profiles": "डेमो प्रोफ़ाइल", "demo_credentials": "डेमो प्रोफ़ाइल विवरण", "use_demo": "डेमो उपयोग करें",
        "demo_farmer": "किसान डेमो", "demo_veterinary": "पशु चिकित्सक डेमो", "demo_government": "सरकारी डेमो",
        "demo_farmer_name": "डेमो किसान", "demo_veterinary_name": "डेमो पशु चिकित्सक", "demo_government_name": "डेमो सरकार",
        "animal_health": "पशु स्वास्थ्य जाँच", "animal_health_desc": "बताए गए लक्षणों से पशु स्वास्थ्य जोखिम जाँचें।",
        "appointments_module": "अपॉइंटमेंट", "appointments_desc": "पशु चिकित्सक से अपॉइंटमेंट बुक और ट्रैक करें।",
        "reports_module": "मेरी रिपोर्ट", "reports_desc": "आपकी जमा की गई पशु स्वास्थ्य रिपोर्ट देखें।",
        "notifications_module": "सूचनाएँ", "notifications_desc": "स्वास्थ्य और अपॉइंटमेंट अपडेट देखें।",
        "animal_care_module": "पशु देखभाल", "animal_care_desc": "पशुओं की सामान्य स्वास्थ्य समस्याओं और देखभाल के बारे में जानें।",
        "animal_reports_module": "पशु रिपोर्ट", "animal_reports_desc": "किसानों द्वारा जमा की गई पशु स्वास्थ्य रिपोर्ट देखें।",
        "appointment_requests_module": "अपॉइंटमेंट अनुरोध", "appointment_requests_desc": "किसानों के पशु चिकित्सा अनुरोधों की समीक्षा और प्रबंधन करें।",
        "laboratory_module": "प्रयोगशाला", "laboratory_desc": "पशु चिकित्सा जाँच और प्रयोगशाला परिणाम जोड़ें।",
        "village_risk_module": "गाँव का जोखिम", "village_risk_desc": "गाँवों में पशु स्वास्थ्य जोखिम की निगरानी करें।",
        "risk_management_module": "जोखिम प्रबंधन", "risk_management_desc": "जोखिम स्तर देखें और कार्रवाई की योजना बनाएँ।",
        "role_caption": "{name} · {role} पोर्टल", "animal_type": "पशु का प्रकार", "appointment_date": "अपॉइंटमेंट की तारीख",
        "appointment_time": "अपॉइंटमेंट का समय", "reason": "अपॉइंटमेंट का कारण", "request_appointment": "अपॉइंटमेंट का अनुरोध करें",
        "enter_reason": "अपॉइंटमेंट का कारण दर्ज करें।", "no_appointment_requests": "अभी कोई अपॉइंटमेंट अनुरोध नहीं है।",
        "no_laboratory_records": "अभी कोई प्रयोगशाला रिकॉर्ड नहीं है।", "care_guidance": "साफ़ पानी और स्वच्छ, छायादार आराम की जगह दें। गंभीर, लगातार या बिगड़ते लक्षणों पर पशु चिकित्सक से संपर्क करें। पशु चिकित्सक की सलाह के बिना दवा न दें।",
        "risk_critical": "गंभीर", "risk_high_concern": "उच्च चिंता", "risk_moderate_concern": "मध्यम चिंता", "risk_mild_concern": "हल्की चिंता",
    },
    "Kannada": {
        "language_label": "ಭಾಷೆ", "profile_heading": "ಪ್ರೊಫೈಲ್", "profile_description": "ನಿಮ್ಮ ಪೋರ್ಟಲ್ ತೆರೆಯಲು ನಿಮ್ಮ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ.",
        "hero_eyebrow": "ಸ್ಮಾರ್ಟ್ ಪಶು ಆರೋಗ್ಯ ಮೇಲ್ವಿಚಾರಣೆ", "back_modules": "ಮಾಡ್ಯೂಲ್‌ಗಳಿಗೆ ಹಿಂತಿರುಗಿ", "demo_data": "ಡೆಮೊ ಡೇಟಾ",
        "demo_profiles": "ಡೆಮೊ ಪ್ರೊಫೈಲ್‌ಗಳು", "demo_credentials": "ಡೆಮೊ ಪ್ರೊಫೈಲ್ ವಿವರಗಳು", "use_demo": "ಡೆಮೊ ಬಳಸಿ",
        "demo_farmer": "ರೈತ ಡೆಮೊ", "demo_veterinary": "ಪಶುವೈದ್ಯ ಡೆಮೊ", "demo_government": "ಸರ್ಕಾರಿ ಡೆಮೊ",
        "demo_farmer_name": "ಡೆಮೊ ರೈತ", "demo_veterinary_name": "ಡೆಮೊ ಪಶುವೈದ್ಯ", "demo_government_name": "ಡೆಮೊ ಸರ್ಕಾರ",
        "animal_health": "ಪಶು ಆರೋಗ್ಯ ಪರಿಶೀಲನೆ", "animal_health_desc": "ವರದಿ ಮಾಡಿದ ಲಕ್ಷಣಗಳಿಂದ ಪಶು ಆರೋಗ್ಯದ ಅಪಾಯ ಪರಿಶೀಲಿಸಿ.",
        "appointments_module": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳು", "appointments_desc": "ಪಶುವೈದ್ಯರ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಬುಕ್ ಮಾಡಿ ಮತ್ತು ಗಮನಿಸಿ.",
        "reports_module": "ನನ್ನ ವರದಿಗಳು", "reports_desc": "ನೀವು ಸಲ್ಲಿಸಿದ ಪಶು ಆರೋಗ್ಯ ವರದಿಗಳನ್ನು ನೋಡಿ.",
        "notifications_module": "ಅಧಿಸೂಚನೆಗಳು", "notifications_desc": "ಆರೋಗ್ಯ ಮತ್ತು ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ನವೀಕರಣಗಳನ್ನು ನೋಡಿ.",
        "animal_care_module": "ಪಶು ಆರೈಕೆ", "animal_care_desc": "ಸಾಮಾನ್ಯ ಪಶು ಆರೋಗ್ಯ ಸಮಸ್ಯೆಗಳು ಮತ್ತು ಆರೈಕೆಯ ಬಗ್ಗೆ ತಿಳಿಯಿರಿ.",
        "animal_reports_module": "ಪಶು ವರದಿಗಳು", "animal_reports_desc": "ರೈತರು ಸಲ್ಲಿಸಿದ ಪಶು ಆರೋಗ್ಯ ವರದಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "appointment_requests_module": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿಗಳು", "appointment_requests_desc": "ರೈತರ ಪಶುವೈದ್ಯಕೀಯ ವಿನಂತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನಿರ್ವಹಿಸಿ.",
        "laboratory_module": "ಪ್ರಯೋಗಾಲಯ", "laboratory_desc": "ಪಶುವೈದ್ಯಕೀಯ ಪರೀಕ್ಷೆ ಮತ್ತು ಪ್ರಯೋಗಾಲಯ ಫಲಿತಾಂಶಗಳನ್ನು ಸೇರಿಸಿ.",
        "village_risk_module": "ಗ್ರಾಮದ ಅಪಾಯ", "village_risk_desc": "ಗ್ರಾಮಗಳಲ್ಲಿನ ಪಶು ಆರೋಗ್ಯ ಅಪಾಯವನ್ನು ಗಮನಿಸಿ.",
        "risk_management_module": "ಅಪಾಯ ನಿರ್ವಹಣೆ", "risk_management_desc": "ಅಪಾಯ ಮಟ್ಟಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಕ್ರಮಗಳನ್ನು ಯೋಜಿಸಿ.",
        "role_caption": "{name} · {role} ಪೋರ್ಟಲ್", "animal_type": "ಪಶುವಿನ ಪ್ರಕಾರ", "appointment_date": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ದಿನಾಂಕ",
        "appointment_time": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಸಮಯ", "reason": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಕಾರಣ", "request_appointment": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿಸಿ",
        "enter_reason": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಕಾರಣವನ್ನು ನಮೂದಿಸಿ.", "no_appointment_requests": "ಇನ್ನೂ ಯಾವುದೇ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿಗಳಿಲ್ಲ.",
        "no_laboratory_records": "ಇನ್ನೂ ಪ್ರಯೋಗಾಲಯ ದಾಖಲೆಗಳಿಲ್ಲ.", "care_guidance": "ಶುದ್ಧ ನೀರು ಮತ್ತು ಸ್ವಚ್ಛ, ನೆರಳಿನ ವಿಶ್ರಾಂತಿ ಸ್ಥಳವನ್ನು ಒದಗಿಸಿ. ಗಂಭೀರ ಅಥವಾ ಹದಗೆಡುತ್ತಿರುವ ಲಕ್ಷಣಗಳಿದ್ದರೆ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ. ಪಶುವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಔಷಧ ನೀಡಬೇಡಿ.",
        "risk_critical": "ಗಂಭೀರ", "risk_high_concern": "ಹೆಚ್ಚಿನ ಚಿಂತೆ", "risk_moderate_concern": "ಮಧ್ಯಮ ಚಿಂತೆ", "risk_mild_concern": "ಕಡಿಮೆ ಚಿಂತೆ",
    },
    "Marathi": {
        "language_label": "भाषा", "profile_heading": "प्रोफाइल", "profile_description": "तुमचे पोर्टल उघडण्यासाठी तपशील भरा.",
        "hero_eyebrow": "स्मार्ट पशुधन आरोग्य निरीक्षण", "back_modules": "मॉड्यूल्सकडे परत जा", "demo_data": "डेमो डेटा",
        "demo_profiles": "डेमो प्रोफाइल", "demo_credentials": "डेमो प्रोफाइल तपशील", "use_demo": "डेमो वापरा",
        "demo_farmer": "शेतकरी डेमो", "demo_veterinary": "पशुवैद्य डेमो", "demo_government": "सरकारी डेमो",
        "demo_farmer_name": "डेमो शेतकरी", "demo_veterinary_name": "डेमो पशुवैद्य", "demo_government_name": "डेमो सरकार",
        "animal_health": "पशु आरोग्य तपासणी", "animal_health_desc": "नोंदवलेल्या लक्षणांवरून पशु आरोग्याचा धोका तपासा.",
        "appointments_module": "भेटी", "appointments_desc": "पशुवैद्यकीय भेट बुक करा आणि तपासा.",
        "reports_module": "माझे अहवाल", "reports_desc": "तुम्ही सादर केलेले पशु आरोग्य अहवाल पाहा.",
        "notifications_module": "सूचना", "notifications_desc": "आरोग्य आणि भेटींचे अपडेट पाहा.",
        "animal_care_module": "पशु काळजी", "animal_care_desc": "सामान्य पशु आरोग्य समस्या आणि काळजीबद्दल जाणून घ्या.",
        "animal_reports_module": "पशु अहवाल", "animal_reports_desc": "शेतकऱ्यांनी सादर केलेले पशु आरोग्य अहवाल तपासा.",
        "appointment_requests_module": "भेटीच्या विनंत्या", "appointment_requests_desc": "शेतकऱ्यांच्या पशुवैद्यकीय विनंत्यांचे पुनरावलोकन आणि व्यवस्थापन करा.",
        "laboratory_module": "प्रयोगशाळा", "laboratory_desc": "पशुवैद्यकीय तपासणी आणि प्रयोगशाळेचे निकाल जोडा.",
        "village_risk_module": "गावाचा धोका", "village_risk_desc": "गावांमधील पशु आरोग्य धोक्याचे निरीक्षण करा.",
        "risk_management_module": "धोका व्यवस्थापन", "risk_management_desc": "धोक्याची पातळी पाहून उपाययोजना आखा.",
        "role_caption": "{name} · {role} पोर्टल", "animal_type": "प्राण्याचा प्रकार", "appointment_date": "भेटीची तारीख",
        "appointment_time": "भेटीची वेळ", "reason": "भेटीचे कारण", "request_appointment": "भेटीची विनंती करा",
        "enter_reason": "भेटीचे कारण लिहा.", "no_appointment_requests": "अद्याप भेटीच्या विनंत्या नाहीत.",
        "no_laboratory_records": "अद्याप प्रयोगशाळेच्या नोंदी नाहीत.", "care_guidance": "स्वच्छ पाणी आणि स्वच्छ, सावलीची विश्रांतीची जागा द्या. गंभीर किंवा वाढणाऱ्या लक्षणांसाठी पशुवैद्याशी संपर्क साधा. पशुवैद्यकीय सल्ल्याशिवाय औषध देऊ नका.",
        "risk_critical": "गंभीर", "risk_high_concern": "उच्च चिंता", "risk_moderate_concern": "मध्यम चिंता", "risk_mild_concern": "कमी चिंता",
    },
    "Telugu": {
        "language_label": "భాష", "profile_heading": "ప్రొఫైల్", "profile_description": "మీ పోర్టల్ తెరవడానికి వివరాలను నమోదు చేయండి.",
        "hero_eyebrow": "స్మార్ట్ పశువుల ఆరోగ్య పర్యవేక్షణ", "back_modules": "మాడ్యూళ్లకు తిరిగి వెళ్లండి", "demo_data": "డెమో డేటా",
        "demo_profiles": "డెమో ప్రొఫైల్స్", "demo_credentials": "డెమో ప్రొఫైల్ వివరాలు", "use_demo": "డెమో ఉపయోగించండి",
        "demo_farmer": "రైతు డెమో", "demo_veterinary": "పశువైద్య డెమో", "demo_government": "ప్రభుత్వ డెమో",
        "demo_farmer_name": "డెమో రైతు", "demo_veterinary_name": "డెమో పశువైద్యుడు", "demo_government_name": "డెమో ప్రభుత్వం",
        "animal_health": "పశు ఆరోగ్య పరీక్ష", "animal_health_desc": "నివేదించిన లక్షణాల ద్వారా పశు ఆరోగ్య ప్రమాదాన్ని పరీక్షించండి.",
        "appointments_module": "అపాయింట్‌మెంట్‌లు", "appointments_desc": "పశువైద్య అపాయింట్‌మెంట్‌లను బుక్ చేసి ట్రాక్ చేయండి.",
        "reports_module": "నా నివేదికలు", "reports_desc": "మీరు సమర్పించిన పశు ఆరోగ్య నివేదికలను చూడండి.",
        "notifications_module": "నోటిఫికేషన్‌లు", "notifications_desc": "ఆరోగ్య మరియు అపాయింట్‌మెంట్ అప్‌డేట్‌లను చూడండి.",
        "animal_care_module": "పశు సంరక్షణ", "animal_care_desc": "సాధారణ పశు ఆరోగ్య సమస్యలు మరియు సంరక్షణ గురించి తెలుసుకోండి.",
        "animal_reports_module": "పశు నివేదికలు", "animal_reports_desc": "రైతులు సమర్పించిన పశు ఆరోగ్య నివేదికలను సమీక్షించండి.",
        "appointment_requests_module": "అపాయింట్‌మెంట్ అభ్యర్థనలు", "appointment_requests_desc": "రైతుల పశువైద్య అభ్యర్థనలను సమీక్షించి నిర్వహించండి.",
        "laboratory_module": "ప్రయోగశాల", "laboratory_desc": "పశువైద్య పరీక్ష మరియు ప్రయోగశాల ఫలితాలను జోడించండి.",
        "village_risk_module": "గ్రామ ప్రమాదం", "village_risk_desc": "గ్రామాల్లో పశు ఆరోగ్య ప్రమాదాన్ని పర్యవేక్షించండి.",
        "risk_management_module": "ప్రమాద నిర్వహణ", "risk_management_desc": "ప్రమాద స్థాయిలను సమీక్షించి చర్యలను ప్రణాళిక చేయండి.",
        "role_caption": "{name} · {role} పోర్టల్", "animal_type": "జంతువు రకం", "appointment_date": "అపాయింట్‌మెంట్ తేదీ",
        "appointment_time": "అపాయింట్‌మెంట్ సమయం", "reason": "అపాయింట్‌మెంట్ కారణం", "request_appointment": "అపాయింట్‌మెంట్ కోరండి",
        "enter_reason": "అపాయింట్‌మెంట్ కారణాన్ని నమోదు చేయండి.", "no_appointment_requests": "ఇంకా అపాయింట్‌మెంట్ అభ్యర్థనలు లేవు.",
        "no_laboratory_records": "ఇంకా ప్రయోగశాల రికార్డులు లేవు.", "care_guidance": "శుభ్రమైన నీరు మరియు శుభ్రమైన నీడగల విశ్రాంతి స్థలాన్ని అందించండి. తీవ్రమైన లేదా అధ్వాన్నమవుతున్న లక్షణాలుంటే పశువైద్యుడిని సంప్రదించండి. పశువైద్యుడి సలహా లేకుండా మందులు ఇవ్వవద్దు.",
        "risk_critical": "తీవ్రమైనది", "risk_high_concern": "అధిక ఆందోళన", "risk_moderate_concern": "మధ్యస్థ ఆందోళన", "risk_mild_concern": "తక్కువ ఆందోళన",
    },
    "Tamil": {
        "language_label": "மொழி", "profile_heading": "சுயவிவரம்", "profile_description": "உங்கள் போர்டலைத் திறக்க விவரங்களை உள்ளிடவும்.",
        "hero_eyebrow": "ஸ்மார்ட் கால்நடை ஆரோக்கிய கண்காணிப்பு", "back_modules": "தொகுதிகளுக்குத் திரும்பு", "demo_data": "டெமோ தரவு",
        "demo_profiles": "டெமோ சுயவிவரங்கள்", "demo_credentials": "டெமோ சுயவிவர விவரங்கள்", "use_demo": "டெமோவைப் பயன்படுத்து",
        "demo_farmer": "விவசாயி டெமோ", "demo_veterinary": "கால்நடை மருத்துவர் டெமோ", "demo_government": "அரசு டெமோ",
        "demo_farmer_name": "டெமோ விவசாயி", "demo_veterinary_name": "டெமோ மருத்துவர்", "demo_government_name": "டெமோ அரசு",
        "animal_health": "கால்நடை ஆரோக்கிய பரிசோதனை", "animal_health_desc": "அறிகுறிகளின் அடிப்படையில் கால்நடை ஆரோக்கிய ஆபத்தைச் சரிபார்க்கவும்.",
        "appointments_module": "சந்திப்புகள்", "appointments_desc": "கால்நடை மருத்துவர் சந்திப்புகளைப் பதிவு செய்து கண்காணிக்கவும்.",
        "reports_module": "என் அறிக்கைகள்", "reports_desc": "நீங்கள் சமர்ப்பித்த கால்நடை ஆரோக்கிய அறிக்கைகளைப் பார்க்கவும்.",
        "notifications_module": "அறிவிப்புகள்", "notifications_desc": "ஆரோக்கியம் மற்றும் சந்திப்பு புதுப்பிப்புகளைப் பார்க்கவும்.",
        "animal_care_module": "கால்நடை பராமரிப்பு", "animal_care_desc": "பொதுவான கால்நடை உடல்நலப் பிரச்சினைகள் மற்றும் பராமரிப்பைப் பற்றி அறியவும்.",
        "animal_reports_module": "கால்நடை அறிக்கைகள்", "animal_reports_desc": "விவசாயிகள் சமர்ப்பித்த கால்நடை ஆரோக்கிய அறிக்கைகளை மதிப்பாய்வு செய்யவும்.",
        "appointment_requests_module": "சந்திப்பு கோரிக்கைகள்", "appointment_requests_desc": "விவசாயிகளின் கால்நடை மருத்துவ கோரிக்கைகளை மதிப்பாய்வு செய்து நிர்வகிக்கவும்.",
        "laboratory_module": "ஆய்வகம்", "laboratory_desc": "கால்நடை பரிசோதனை மற்றும் ஆய்வக முடிவுகளைச் சேர்க்கவும்.",
        "village_risk_module": "கிராம அபாயம்", "village_risk_desc": "கிராமங்களில் கால்நடை ஆரோக்கிய ஆபத்தை கண்காணிக்கவும்.",
        "risk_management_module": "ஆபத்து மேலாண்மை", "risk_management_desc": "ஆபத்து நிலைகளை மதிப்பாய்வு செய்து நடவடிக்கைகளைத் திட்டமிடவும்.",
        "role_caption": "{name} · {role} போர்டல்", "animal_type": "விலங்கு வகை", "appointment_date": "சந்திப்பு தேதி",
        "appointment_time": "சந்திப்பு நேரம்", "reason": "சந்திப்பிற்கான காரணம்", "request_appointment": "சந்திப்பைக் கோரவும்",
        "enter_reason": "சந்திப்பிற்கான காரணத்தை உள்ளிடவும்.", "no_appointment_requests": "சந்திப்பு கோரிக்கைகள் எதுவும் இல்லை.",
        "no_laboratory_records": "ஆய்வக பதிவுகள் எதுவும் இல்லை.", "care_guidance": "சுத்தமான தண்ணீர் மற்றும் சுத்தமான நிழலான ஓய்வு இடத்தை வழங்கவும். கடுமையான அல்லது மோசமடையும் அறிகுறிகளுக்கு கால்நடை மருத்துவரை அணுகவும். மருத்துவரின் ஆலோசனையின்றி மருந்து கொடுக்க வேண்டாம்.",
        "risk_critical": "மிகக் கடுமை", "risk_high_concern": "அதிக கவலை", "risk_moderate_concern": "மிதமான கவலை", "risk_mild_concern": "குறைந்த கவலை",
    },
}
for language_name, translations in TRANSLATION_EXTRAS.items():
    TRANSLATIONS[language_name].update(translations)

ANIMAL_CARE_TRANSLATIONS = {
    "English": {
        "care_guide_title": "Animal Care and Disease Guide", "care_choose_animal": "Choose an animal", "care_choose_topic": "Choose a health concern",
        "care_supportive_label": "Safe supportive care", "care_urgent_label": "Get veterinary help urgently if", "care_species_note": "Species-specific warning",
        "care_scope_note": "This guide covers common warning patterns, not every disease. Similar signs can have different causes; a veterinarian must diagnose and prescribe treatment.",
        "care_no_treatment": "Do not give human or leftover medicines, force food or water, or apply chemicals/remedies unless a veterinarian directs you.",
        "care_urgent_signs": "Trouble breathing, collapse, seizures, uncontrolled bleeding, severe swelling, inability to urinate, rapid worsening, or several animals becoming ill suddenly needs urgent veterinary attention.",
        "care_bloat_title": "Bloat or abdominal swelling", "care_reproductive_title": "Reproductive or birth problem", "care_toxin_title": "Possible poisoning or toxin exposure",
        "care_flock_title": "Flock illness or sudden deaths", "care_egg_title": "Egg production or laying change", "care_urinary_title": "Urinary or reproductive change",
        "care_colic_title": "Colic or severe abdominal pain", "care_rabbit_gi_title": "Reduced eating or droppings (gut slowdown)", "care_dental_title": "Dental or chewing problem",
        "care_group_ruminant": "In cattle, buffalo, goats, sheep and camels, sudden abdominal swelling, inability to stand, mouth sores with drooling/lameness, or several sick animals needs prompt veterinary assessment. Do not puncture a swollen abdomen or move sick animals between herds.",
        "care_group_poultry": "For chickens, ducks, turkeys and pigeons, isolate visibly sick birds if safe, use separate feed/water equipment, and contact a veterinarian promptly for several affected birds or any sudden deaths. Avoid moving birds between flocks.",
        "care_group_swine": "For pigs, fever with coughing/diarrhea, unusual skin discoloration, several sick animals or sudden deaths needs urgent veterinary/animal-health advice. Restrict movement of pigs and equipment until advised.",
        "care_group_companion": "For dogs and cats, suspected toxin exposure, collapse, repeated vomiting, breathing trouble, or inability to pass urine is urgent. Do not induce vomiting or give human medicines unless a veterinarian instructs you.",
        "care_group_equine": "For horses and donkeys, pawing, repeated rolling, looking at the flank, sweating or passing little/no manure can indicate colic and is an emergency. Call a veterinarian; do not give medicines or force exercise.",
        "care_group_rabbit": "For rabbits, not eating or reduced/no droppings can become an emergency quickly. Contact a veterinarian promptly; keep the rabbit calm with hay and water available, and do not force-feed unless instructed.",
    },
    "Hindi": {
        "care_guide_title": "पशु देखभाल और रोग मार्गदर्शिका", "care_choose_animal": "पशु चुनें", "care_choose_topic": "स्वास्थ्य समस्या चुनें",
        "care_supportive_label": "सुरक्षित सहायक देखभाल", "care_urgent_label": "इन स्थितियों में तुरंत पशु चिकित्सक से संपर्क करें", "care_species_note": "इस प्रजाति के लिए विशेष चेतावनी",
        "care_scope_note": "यह मार्गदर्शिका सामान्य चेतावनी संकेतों को बताती है, हर रोग को नहीं। एक जैसे लक्षणों के अलग कारण हो सकते हैं; निदान और उपचार पशु चिकित्सक ही करें।",
        "care_no_treatment": "पशु चिकित्सक के निर्देश के बिना इंसानी या बची हुई दवा न दें, जबरन खाना-पानी न दें और घरेलू रसायन/नुस्खे न लगाएँ।",
        "care_urgent_signs": "साँस लेने में कठिनाई, बेहोशी/गिरना, दौरे, न रुकने वाला खून, तेज सूजन, पेशाब न कर पाना, तेजी से बिगड़ना या कई पशुओं का अचानक बीमार होना तुरंत पशु चिकित्सा सहायता माँगता है।",
        "care_bloat_title": "पेट फूलना या पेट में सूजन", "care_reproductive_title": "प्रजनन या प्रसव की समस्या", "care_toxin_title": "ज़हर या विषैले पदार्थ का संदेह",
        "care_flock_title": "झुंड में बीमारी या अचानक मृत्यु", "care_egg_title": "अंडे देने या उत्पादन में बदलाव", "care_urinary_title": "मूत्र या प्रजनन में बदलाव",
        "care_colic_title": "पेट का तेज दर्द या कोलिक", "care_rabbit_gi_title": "कम खाना या मल कम होना (आँतों की गति धीमी)", "care_dental_title": "दाँत या चबाने की समस्या",
        "care_group_ruminant": "गाय, भैंस, बकरी, भेड़ और ऊँट में अचानक पेट फूलना, खड़ा न हो पाना, लार के साथ मुँह के घाव/लंगड़ापन या कई पशुओं का बीमार होना जल्दी पशु चिकित्सक को दिखाएँ। सूजे पेट में छेद न करें और बीमार पशुओं को झुंडों के बीच न ले जाएँ।",
        "care_group_poultry": "मुर्गी, बतख, टर्की और कबूतर में बीमार पक्षी को सुरक्षित हो तो अलग रखें, पानी/चारे के बर्तन अलग रखें और कई पक्षियों के बीमार होने या अचानक मृत्यु पर पशु चिकित्सक से तुरंत संपर्क करें। पक्षियों को झुंडों के बीच न ले जाएँ।",
        "care_group_swine": "सूअरों में बुखार के साथ खाँसी/दस्त, त्वचा का असामान्य रंग, कई पशुओं का बीमार होना या अचानक मृत्यु होने पर तुरंत पशु चिकित्सक/पशु-स्वास्थ्य सेवा से सलाह लें। सलाह मिलने तक पशु और उपकरणों की आवाजाही रोकें।",
        "care_group_companion": "कुत्ते और बिल्ली में ज़हर का संदेह, गिरना, बार-बार उल्टी, साँस की तकलीफ़ या पेशाब न कर पाना आपात स्थिति है। पशु चिकित्सक के निर्देश के बिना उल्टी न कराएँ और इंसानी दवा न दें।",
        "care_group_equine": "घोड़े और गधे में पैर पटकना, बार-बार लोटना, पेट की ओर देखना, पसीना या मल न निकलना कोलिक का संकेत हो सकता है और आपात स्थिति है। पशु चिकित्सक को बुलाएँ; दवा न दें और जबरन व्यायाम न कराएँ।",
        "care_group_rabbit": "खरगोश का खाना बंद करना या मल कम/बंद होना जल्दी आपात स्थिति बन सकता है। जल्द पशु चिकित्सक से संपर्क करें; खरगोश को शांत रखें और घास-पानी उपलब्ध रखें। निर्देश के बिना जबरन खाना न खिलाएँ।",
    },
    "Kannada": {
        "care_guide_title": "ಪಶು ಆರೈಕೆ ಮತ್ತು ರೋಗ ಮಾರ್ಗದರ್ಶಿ", "care_choose_animal": "ಪಶುವನ್ನು ಆಯ್ಕೆಮಾಡಿ", "care_choose_topic": "ಆರೋಗ್ಯ ಸಮಸ್ಯೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "care_supportive_label": "ಸುರಕ್ಷಿತ ಸಹಾಯಕ ಆರೈಕೆ", "care_urgent_label": "ಈ ಲಕ್ಷಣಗಳಿದ್ದರೆ ತಕ್ಷಣ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ", "care_species_note": "ಈ ಪ್ರಾಣಿಗೆ ವಿಶೇಷ ಎಚ್ಚರಿಕೆ",
        "care_scope_note": "ಈ ಮಾರ್ಗದರ್ಶಿ ಸಾಮಾನ್ಯ ಎಚ್ಚರಿಕೆ ಲಕ್ಷಣಗಳನ್ನು ಒಳಗೊಂಡಿದೆ, ಪ್ರತಿಯೊಂದು ರೋಗವನ್ನಲ್ಲ. ಒಂದೇ ಲಕ್ಷಣಕ್ಕೆ ಬೇರೆ ಕಾರಣಗಳಿರಬಹುದು; ರೋಗನಿರ್ಣಯ ಮತ್ತು ಚಿಕಿತ್ಸೆ ಪಶುವೈದ್ಯರಿಂದಲೇ ಆಗಬೇಕು.",
        "care_no_treatment": "ಪಶುವೈದ್ಯರ ಸೂಚನೆಯಿಲ್ಲದೆ ಮಾನವರ ಅಥವಾ ಉಳಿದ ಔಷಧಿ ನೀಡಬೇಡಿ, ಬಲವಂತವಾಗಿ ಆಹಾರ/ನೀರು ಕೊಡಬೇಡಿ ಅಥವಾ ರಾಸಾಯನಿಕ/ಮನೆಮದ್ದನ್ನು ಹಚ್ಚಬೇಡಿ.",
        "care_urgent_signs": "ಉಸಿರಾಟದ ತೊಂದರೆ, ಕುಸಿದು ಬೀಳುವುದು, ಸೆಳೆತ, ನಿಲ್ಲದ ರಕ್ತಸ್ರಾವ, ತೀವ್ರ ಊತ, ಮೂತ್ರ ವಿಸರ್ಜನೆ ಆಗದಿರುವುದು, ವೇಗವಾಗಿ ಹದಗೆಡುವುದು ಅಥವಾ ಹಲವು ಪಶುಗಳು ಒಟ್ಟಿಗೆ ಅಸ್ವಸ್ಥವಾಗುವುದು ತುರ್ತು ಪಶುವೈದ್ಯಕೀಯ ನೆರವನ್ನು ಅಗತ್ಯಪಡಿಸುತ್ತದೆ.",
        "care_bloat_title": "ಹೊಟ್ಟೆ ಉಬ್ಬರ ಅಥವಾ ಊತ", "care_reproductive_title": "ಸಂತಾನೋತ್ಪತ್ತಿ ಅಥವಾ ಹೆರಿಗೆ ಸಮಸ್ಯೆ", "care_toxin_title": "ವಿಷ ಅಥವಾ ವಿಷಕಾರಿ ವಸ್ತುವಿನ ಶಂಕೆ",
        "care_flock_title": "ಹಿಂಡಿನ ಕಾಯಿಲೆ ಅಥವಾ ಹಠಾತ್ ಸಾವುಗಳು", "care_egg_title": "ಮೊಟ್ಟೆ ಉತ್ಪಾದನೆ ಅಥವಾ ಇಡುವಿಕೆಯಲ್ಲಿ ಬದಲಾವಣೆ", "care_urinary_title": "ಮೂತ್ರ ಅಥವಾ ಸಂತಾನೋತ್ಪತ್ತಿಯಲ್ಲಿ ಬದಲಾವಣೆ",
        "care_colic_title": "ತೀವ್ರ ಹೊಟ್ಟೆ ನೋವು (ಕಾಲಿಕ್)", "care_rabbit_gi_title": "ಕಡಿಮೆ ತಿನ್ನುವುದು ಅಥವಾ ಮಲ ಕಡಿಮೆಯಾಗುವುದು", "care_dental_title": "ಹಲ್ಲು ಅಥವಾ ಜಗಿಯುವ ಸಮಸ್ಯೆ",
        "care_group_ruminant": "ಹಸು, ಎಮ್ಮೆ, ಮೇಕೆ, ಕುರಿ ಮತ್ತು ಒಂಟೆಯಲ್ಲಿ ಹಠಾತ್ ಹೊಟ್ಟೆ ಉಬ್ಬರ, ನಿಲ್ಲಲಾಗದಿರುವುದು, ಬಾಯಿಯ ಗಾಯಗಳ ಜೊತೆಗೆ ಲಾಲಾರಸ/ಕುಂಟು ಅಥವಾ ಹಲವು ಪಶುಗಳು ಅಸ್ವಸ್ಥವಾಗುವುದು ಕಂಡರೆ ತಕ್ಷಣ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ. ಊದಿದ ಹೊಟ್ಟೆಗೆ ರಂಧ್ರ ಮಾಡಬೇಡಿ; ಅಸ್ವಸ್ಥ ಪಶುಗಳನ್ನು ಹಿಂಡುಗಳ ನಡುವೆ ಸಾಗಿಸಬೇಡಿ.",
        "care_group_poultry": "ಕೋಳಿ, ಬಾತುಕೋಳಿ, ಟರ್ಕಿ ಮತ್ತು ಪಾರಿವಾಳದಲ್ಲಿ ಅಸ್ವಸ್ಥ ಪಕ್ಷಿಯನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಸಾಧ್ಯವಾದರೆ ಪ್ರತ್ಯೇಕಿಸಿ, ಆಹಾರ/ನೀರಿನ ಪಾತ್ರೆಗಳನ್ನು ಬೇರ್ಪಡಿಸಿ. ಹಲವು ಪಕ್ಷಿಗಳು ಅಸ್ವಸ್ಥವಾದರೆ ಅಥವಾ ಹಠಾತ್ ಸಾವುಗಳಿದ್ದರೆ ತಕ್ಷಣ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ. ಪಕ್ಷಿಗಳನ್ನು ಹಿಂಡುಗಳ ನಡುವೆ ಸಾಗಿಸಬೇಡಿ.",
        "care_group_swine": "ಹಂದಿಗಳಲ್ಲಿ ಜ್ವರದೊಂದಿಗೆ ಕೆಮ್ಮು/ಅತಿಸಾರ, ಚರ್ಮದ ಅಸಹಜ ಬಣ್ಣ, ಹಲವು ಹಂದಿಗಳು ಅಸ್ವಸ್ಥವಾಗುವುದು ಅಥವಾ ಹಠಾತ್ ಸಾವು ಕಂಡರೆ ತಕ್ಷಣ ಪಶುವೈದ್ಯ/ಪಶು ಆರೋಗ್ಯ ಸೇವೆಯನ್ನು ಸಂಪರ್ಕಿಸಿ. ಸಲಹೆ ಸಿಗುವವರೆಗೆ ಹಂದಿ ಮತ್ತು ಉಪಕರಣಗಳ ಚಲನವಲನವನ್ನು ನಿಲ್ಲಿಸಿ.",
        "care_group_companion": "ನಾಯಿ ಮತ್ತು ಬೆಕ್ಕಿನಲ್ಲಿ ವಿಷದ ಶಂಕೆ, ಕುಸಿತ, ಮರುಮರು ವಾಂತಿ, ಉಸಿರಾಟದ ತೊಂದರೆ ಅಥವಾ ಮೂತ್ರ ವಿಸರ್ಜನೆ ಆಗದಿರುವುದು ತುರ್ತು. ಪಶುವೈದ್ಯರ ಸೂಚನೆಯಿಲ್ಲದೆ ವಾಂತಿ ಮಾಡಿಸಬೇಡಿ ಅಥವಾ ಮಾನವರ ಔಷಧಿ ನೀಡಬೇಡಿ.",
        "care_group_equine": "ಕುದುರೆ ಮತ್ತು ಕತ್ತೆಯಲ್ಲಿ ಕಾಲಿನಿಂದ ನೆಲ ಕೆರೆಯುವುದು, ಮರುಮರು ಉರುಳುವುದು, ಹೊಟ್ಟೆಯ ಕಡೆ ನೋಡುವುದು, ಬೆವರುವುದು ಅಥವಾ ಮಲ ಬರದಿರುವುದು ಕಾಲಿಕ್ ಸೂಚನೆಯಾಗಿರಬಹುದು; ಇದು ತುರ್ತು. ಪಶುವೈದ್ಯರನ್ನು ಕರೆಸಿ; ಔಷಧಿ ಕೊಡಬೇಡಿ ಅಥವಾ ಬಲವಂತವಾಗಿ ವ್ಯಾಯಾಮ ಮಾಡಿಸಬೇಡಿ.",
        "care_group_rabbit": "ಮೊಲ ತಿನ್ನದಿರುವುದು ಅಥವಾ ಮಲ ಕಡಿಮೆಯಾಗುವುದು/ನಿಲ್ಲುವುದು ಬೇಗ ತುರ್ತು ಸ್ಥಿತಿಯಾಗಬಹುದು. ತಕ್ಷಣ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ; ಮೊಲವನ್ನು ಶಾಂತವಾಗಿಟ್ಟು ಹುಲ್ಲು ಮತ್ತು ನೀರು ಲಭ್ಯವಿರಲಿ. ಸೂಚನೆಯಿಲ್ಲದೆ ಬಲವಂತವಾಗಿ ಆಹಾರ ಕೊಡಬೇಡಿ.",
    },
    "Marathi": {
        "care_guide_title": "पशु काळजी आणि रोग मार्गदर्शक", "care_choose_animal": "प्राणी निवडा", "care_choose_topic": "आरोग्य समस्या निवडा",
        "care_supportive_label": "सुरक्षित सहाय्यक काळजी", "care_urgent_label": "ही लक्षणे असल्यास तातडीने पशुवैद्याशी संपर्क करा", "care_species_note": "या प्राण्यासाठी विशेष सूचना",
        "care_scope_note": "या मार्गदर्शकात सामान्य धोक्याची लक्षणे आहेत, प्रत्येक रोग नाही. समान लक्षणांची कारणे वेगवेगळी असू शकतात; निदान व उपचार पशुवैद्यानेच करावेत.",
        "care_no_treatment": "पशुवैद्याच्या सूचनेशिवाय मानवी किंवा उरलेली औषधे देऊ नका, जबरदस्तीने खाऊ-पिऊ घालू नका किंवा रसायने/घरगुती उपाय लावू नका.",
        "care_urgent_signs": "श्वास घेण्यास त्रास, कोसळणे, झटके, न थांबणारा रक्तस्राव, तीव्र सूज, लघवी न होणे, वेगाने बिघडणारी स्थिती किंवा अनेक पशू अचानक आजारी पडणे यासाठी तातडीची पशुवैद्यकीय मदत घ्या.",
        "care_bloat_title": "पोट फुगणे किंवा सूज", "care_reproductive_title": "प्रजनन किंवा प्रसूतीची समस्या", "care_toxin_title": "विष किंवा विषारी पदार्थाचा संशय",
        "care_flock_title": "कळपातील आजार किंवा अचानक मृत्यू", "care_egg_title": "अंडी देणे किंवा उत्पादनातील बदल", "care_urinary_title": "लघवी किंवा प्रजननातील बदल",
        "care_colic_title": "पोटदुखी किंवा कॉलिक", "care_rabbit_gi_title": "कमी खाणे किंवा विष्ठा कमी होणे", "care_dental_title": "दात किंवा चावण्याची समस्या",
        "care_group_ruminant": "गाय, म्हैस, शेळी, मेंढी आणि उंटात अचानक पोट फुगणे, उभे राहता न येणे, तोंडातील जखमांसह लाळ/लंगडणे किंवा अनेक पशू आजारी पडणे दिसल्यास तातडीने पशुवैद्याशी संपर्क करा. फुगलेल्या पोटाला छिद्र पाडू नका; आजारी पशूंना कळपांमध्ये हलवू नका.",
        "care_group_poultry": "कोंबडी, बदक, टर्की आणि कबूतरांमध्ये शक्य असल्यास आजारी पक्षी वेगळे ठेवा, खाद्य/पाण्याची भांडी वेगळी वापरा. अनेक पक्षी आजारी पडल्यास किंवा अचानक मृत्यू झाल्यास तातडीने पशुवैद्याशी संपर्क करा. पक्ष्यांना कळपांमध्ये हलवू नका.",
        "care_group_swine": "डुकरांना तापासह खोकला/जुलाब, त्वचेचा असामान्य रंग, अनेक डुकरे आजारी पडणे किंवा अचानक मृत्यू झाल्यास तातडीने पशुवैद्य/पशु-आरोग्य सेवेशी संपर्क करा. सल्ला मिळेपर्यंत डुकरे व उपकरणांची हालचाल थांबवा.",
        "care_group_companion": "कुत्रा किंवा मांजरीत विषबाधेचा संशय, कोसळणे, वारंवार उलटी, श्वास घेण्यास त्रास किंवा लघवी न होणे ही तातडीची स्थिती आहे. पशुवैद्याच्या सूचनेशिवाय उलटी करवू नका किंवा मानवी औषधे देऊ नका.",
        "care_group_equine": "घोडा किंवा गाढव वारंवार पाय आपटत असेल/लोळत असेल, पोटाकडे पाहत असेल, घाम येत असेल किंवा शेण होत नसेल तर कॉलिक असू शकतो; ही आपत्कालीन स्थिती आहे. पशुवैद्याला बोलवा; औषध देऊ नका किंवा जबरदस्तीने व्यायाम करवू नका.",
        "care_group_rabbit": "ससा खाणे बंद करणे किंवा विष्ठा कमी/बंद होणे लवकरच आपत्कालीन ठरू शकते. तातडीने पशुवैद्याशी संपर्क करा; सशाला शांत ठेवा आणि गवत-पाणी उपलब्ध ठेवा. सूचनेशिवाय जबरदस्तीने खाऊ घालू नका.",
    },
    "Telugu": {
        "care_guide_title": "పశు సంరక్షణ మరియు వ్యాధి మార్గదర్శిని", "care_choose_animal": "జంతువును ఎంచుకోండి", "care_choose_topic": "ఆరోగ్య సమస్యను ఎంచుకోండి",
        "care_supportive_label": "సురక్షిత సహాయక సంరక్షణ", "care_urgent_label": "ఈ లక్షణాలుంటే వెంటనే పశువైద్యుడిని సంప్రదించండి", "care_species_note": "ఈ జంతువుకు ప్రత్యేక హెచ్చరిక",
        "care_scope_note": "ఈ మార్గదర్శిని సాధారణ హెచ్చరిక సంకేతాలను మాత్రమే కవర్ చేస్తుంది; ప్రతి వ్యాధిని కాదు. ఒకే లక్షణాలకు వేర్వేరు కారణాలు ఉండవచ్చు; నిర్ధారణ మరియు చికిత్సను పశువైద్యుడే నిర్ణయించాలి.",
        "care_no_treatment": "పశువైద్యుడి సూచన లేకుండా మానవుల లేదా మిగిలిన మందులు ఇవ్వవద్దు, బలవంతంగా ఆహారం/నీరు పెట్టవద్దు, రసాయనాలు/ఇంటి చికిత్సలు వాడవద్దు.",
        "care_urgent_signs": "శ్వాస ఇబ్బంది, కుప్పకూలడం, మూర్ఛలు, ఆగని రక్తస్రావం, తీవ్రమైన వాపు, మూత్రం చేయలేకపోవడం, వేగంగా క్షీణించడం లేదా అనేక జంతువులు అకస్మాత్తుగా అనారోగ్యం పాలవడం అత్యవసర పశువైద్య సహాయం అవసరమని సూచిస్తాయి.",
        "care_bloat_title": "కడుపు ఉబ్బరం లేదా వాపు", "care_reproductive_title": "పునరుత్పత్తి లేదా ప్రసవ సమస్య", "care_toxin_title": "విషం లేదా విషపదార్థం అనుమానం",
        "care_flock_title": "మందలో వ్యాధి లేదా ఆకస్మిక మరణాలు", "care_egg_title": "గుడ్లు పెట్టడం లేదా ఉత్పత్తిలో మార్పు", "care_urinary_title": "మూత్ర లేదా పునరుత్పత్తి మార్పు",
        "care_colic_title": "తీవ్రమైన కడుపు నొప్పి (కోలిక్)", "care_rabbit_gi_title": "తక్కువగా తినడం లేదా విసర్జన తగ్గడం", "care_dental_title": "పళ్లు లేదా నమలడంలో సమస్య",
        "care_group_ruminant": "ఆవు, గేదె, మేక, గొర్రె, ఒంటెలలో అకస్మాత్తుగా కడుపు ఉబ్బడం, నిలబడలేకపోవడం, నోటి పుండ్లతో లాలాజలం/కుంటడం లేదా అనేక జంతువులు అనారోగ్యం పాలవడం కనిపిస్తే వెంటనే పశువైద్యుడిని సంప్రదించండి. ఉబ్బిన కడుపును గుచ్చవద్దు; అనారోగ్య జంతువులను మందల మధ్య తరలించవద్దు.",
        "care_group_poultry": "కోళ్లు, బాతులు, టర్కీలు, పావురాల్లో వీలైతే అనారోగ్య పక్షులను వేరుగా ఉంచండి; ఆహారం/నీటి పాత్రలను వేరుగా వాడండి. అనేక పక్షులు అనారోగ్యంగా ఉంటే లేదా ఆకస్మిక మరణాలుంటే వెంటనే పశువైద్యుడిని సంప్రదించండి. పక్షులను మందల మధ్య తరలించవద్దు.",
        "care_group_swine": "పందుల్లో జ్వరంతో దగ్గు/విరేచనాలు, చర్మం రంగు మారడం, అనేక పందులు అనారోగ్యం పాలవడం లేదా ఆకస్మిక మరణాలు ఉంటే వెంటనే పశువైద్య/పశు ఆరోగ్య సేవను సంప్రదించండి. సూచన వచ్చే వరకు పందులు, పరికరాల కదలికను పరిమితం చేయండి.",
        "care_group_companion": "కుక్కలు, పిల్లుల్లో విషపదార్థం అనుమానం, కుప్పకూలడం, పదేపదే వాంతులు, శ్వాస ఇబ్బంది లేదా మూత్రం చేయలేకపోవడం అత్యవసరం. పశువైద్యుడి సూచన లేకుండా వాంతి చేయించవద్దు లేదా మానవుల మందులు ఇవ్వవద్దు.",
        "care_group_equine": "గుర్రం లేదా గాడిద నేలను తన్నడం, పదేపదే దొర్లడం, పొట్టవైపు చూడడం, చెమటలు పట్టడం లేదా పేడ వేయకపోవడం కోలిక్ సూచన కావచ్చు; ఇది అత్యవసరం. పశువైద్యుడిని పిలవండి; మందులు ఇవ్వవద్దు లేదా బలవంతంగా వ్యాయామం చేయించవద్దు.",
        "care_group_rabbit": "కుందేలు తినకపోవడం లేదా విసర్జన తగ్గడం/ఆగిపోవడం త్వరగా అత్యవసరంగా మారవచ్చు. వెంటనే పశువైద్యుడిని సంప్రదించండి; ప్రశాంతంగా ఉంచి గడ్డి, నీరు అందుబాటులో ఉంచండి. సూచన లేకుండా బలవంతంగా ఆహారం పెట్టవద్దు.",
    },
    "Tamil": {
        "care_guide_title": "கால்நடை பராமரிப்பு மற்றும் நோய் வழிகாட்டி", "care_choose_animal": "விலங்கைத் தேர்ந்தெடுக்கவும்", "care_choose_topic": "உடல்நலப் பிரச்சினையைத் தேர்ந்தெடுக்கவும்",
        "care_supportive_label": "பாதுகாப்பான ஆதரவு பராமரிப்பு", "care_urgent_label": "இந்த அறிகுறிகள் இருந்தால் உடனடியாக கால்நடை மருத்துவரை அணுகவும்", "care_species_note": "இந்த விலங்குக்கான சிறப்பு எச்சரிக்கை",
        "care_scope_note": "இந்த வழிகாட்டி பொதுவான எச்சரிக்கை அறிகுறிகளை மட்டுமே உள்ளடக்குகிறது; எல்லா நோய்களையும் அல்ல. ஒரே அறிகுறிக்கு பல காரணங்கள் இருக்கலாம்; நோயறிதல் மற்றும் சிகிச்சையை கால்நடை மருத்துவரே தீர்மானிக்க வேண்டும்.",
        "care_no_treatment": "மருத்துவர் அறிவுறுத்தாமல் மனிதர்களுக்கான அல்லது மீதமுள்ள மருந்துகளை கொடுக்காதீர்கள்; வலுக்கட்டாயமாக உணவு/தண்ணீர் கொடுக்காதீர்கள்; ரசாயனங்கள்/வீட்டு வைத்தியங்களைப் பயன்படுத்தாதீர்கள்.",
        "care_urgent_signs": "சுவாச சிரமம், மயங்கி விழுதல், வலிப்பு, நிற்காத இரத்தப்போக்கு, கடுமையான வீக்கம், சிறுநீர் கழிக்க முடியாமை, விரைவாக மோசமாதல் அல்லது பல விலங்குகள் திடீரென நோய்வாய்ப்படுதல் அவசர கால்நடை மருத்துவ உதவி தேவை என்பதைக் குறிக்கும்.",
        "care_bloat_title": "வயிறு உப்புசம் அல்லது வீக்கம்", "care_reproductive_title": "இனப்பெருக்கம் அல்லது பிரசவப் பிரச்சினை", "care_toxin_title": "நச்சு அல்லது விஷப்பொருள் சந்தேகம்",
        "care_flock_title": "கூட்டத்தில் நோய் அல்லது திடீர் இறப்புகள்", "care_egg_title": "முட்டையிடுதல் அல்லது உற்பத்தி மாற்றம்", "care_urinary_title": "சிறுநீர் அல்லது இனப்பெருக்க மாற்றம்",
        "care_colic_title": "கடுமையான வயிற்று வலி (கோலிக்)", "care_rabbit_gi_title": "குறைவாக உண்பது அல்லது கழிவு குறைதல்", "care_dental_title": "பல் அல்லது மெல்லும் பிரச்சினை",
        "care_group_ruminant": "பசு, எருமை, ஆடு, செம்மறியாடு, ஒட்டகத்தில் திடீர் வயிற்று வீக்கம், நிற்க முடியாமை, வாய்ப்புண்களுடன் உமிழ்நீர்/நொண்டுதல் அல்லது பல விலங்குகள் நோய்வாய்ப்படுதல் இருந்தால் உடனடியாக மருத்துவரை அணுகவும். வீங்கிய வயிற்றைத் துளைக்காதீர்கள்; நோய்வாய்ப்பட்ட விலங்குகளை கூட்டங்களுக்கு இடையே நகர்த்தாதீர்கள்.",
        "care_group_poultry": "கோழி, வாத்து, வான்கோழி, புறாக்களில் நோய்வாய்ப்பட்ட பறவைகளை பாதுகாப்பாக இருந்தால் தனியாக வைக்கவும்; உணவு/தண்ணீர் பாத்திரங்களைப் பிரிக்கவும். பல பறவைகள் நோயுற்றாலோ திடீர் இறப்புகள் ஏற்பட்டாலோ உடனே மருத்துவரை அணுகவும். பறவைகளை கூட்டங்களுக்கு இடையே நகர்த்தாதீர்கள்.",
        "care_group_swine": "பன்றிகளில் காய்ச்சலுடன் இருமல்/வயிற்றுப்போக்கு, தோல் நிறமாற்றம், பல பன்றிகள் நோய்வாய்ப்படுதல் அல்லது திடீர் இறப்புகள் இருந்தால் உடனடியாக கால்நடை/விலங்கு சுகாதார சேவையை அணுகவும். அறிவுரை கிடைக்கும் வரை பன்றிகள் மற்றும் உபகரணங்களின் நகர்வைக் கட்டுப்படுத்தவும்.",
        "care_group_companion": "நாய் அல்லது பூனையில் நச்சு உட்கொண்ட சந்தேகம், மயங்கி விழுதல், மீண்டும் மீண்டும் வாந்தி, சுவாச சிரமம் அல்லது சிறுநீர் கழிக்க முடியாமை அவசர நிலை. மருத்துவர் கூறாமல் வாந்தி வரவழைக்கவோ மனித மருந்து கொடுக்கவோ வேண்டாம்.",
        "care_group_equine": "குதிரை அல்லது கழுதை தரையை உதைத்தல், மீண்டும் மீண்டும் உருளுதல், வயிற்றைப் பார்த்தல், வியர்த்தல் அல்லது சாணம் வெளியேறாமை கோலிக் அறிகுறியாக இருக்கலாம்; இது அவசரம். மருத்துவரை அழைக்கவும்; மருந்து கொடுக்கவோ கட்டாயமாக உடற்பயிற்சி செய்யவோ வேண்டாம்.",
        "care_group_rabbit": "முயல் உண்பதை நிறுத்துதல் அல்லது கழிவு குறைதல்/நிற்றல் விரைவில் அவசரமாகலாம். உடனே மருத்துவரை அணுகவும்; முயலை அமைதியாக வைத்து வைக்கோல், தண்ணீர் கிடைக்கச் செய்யவும். அறிவுறுத்தாமல் வலுக்கட்டாயமாக உணவளிக்க வேண்டாம்.",
    },
}
for language_name, translations in ANIMAL_CARE_TRANSLATIONS.items():
    TRANSLATIONS[language_name].update(translations)

CUSTOM_CSS = """
<style>
    #MainMenu, header, footer { display: none !important; }
    .stApp { background: linear-gradient(135deg, #f9fbfa 0%, #edf8f2 100%); color: #173d2e !important; }
    .stApp [data-testid="stMarkdownContainer"], .stApp label, .stApp p,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp [data-testid="stMetricLabel"] {
        color: #173d2e !important;
    }
    .block-container { max-width: 1200px !important; padding-top: 1rem !important; }
    .topbar-shell { background: rgba(255,255,255,0.96); border: 1px solid #dfeae2; border-radius: 20px; padding: 0.8rem 1rem; box-shadow: 0 12px 28px rgba(17,59,42,0.05); margin-bottom: 1rem; }
    .hero-shell { background: linear-gradient(135deg, #ffffff 0%, #edf9f1 100%); border: 1px solid #dfeae2; border-radius: 30px; padding: 2.2rem; box-shadow: 0 18px 40px rgba(17,58,42,0.08); }
    .eyebrow { display: inline-block; background: #dff4e6; color: #176d42; border-radius: 999px; padding: 0.46rem 0.8rem; font-size: 0.72rem; letter-spacing: 0.1em; font-weight: 800; text-transform: uppercase; }
    .hero-title { font-size: clamp(2.4rem, 5vw, 4.2rem); line-height: 1.05; margin: 0.9rem 0 0.5rem; color: #123d2d; }
    .hero-subtitle { font-size: 1.12rem; color: #586f67; }
    .feature-card, .portal-card, .report-card { background: rgba(255,255,255,0.97); border: 1px solid #ddeae0; border-radius: 22px; padding: 1.2rem; box-shadow: 0 12px 32px rgba(17,59,42,0.06); }
    .feature-card h3, .portal-card h3 { margin: 0.7rem 0 0.3rem; color: #173f31; }
    .feature-card p, .portal-card p, .report-card p { margin: 0; color: #5a6d64; }
    .tag { display: inline-block; background: #edf9f1; color: #196c45; border-radius: 999px; padding: 0.38rem 0.72rem; font-size: 0.68rem; letter-spacing: 0.08em; font-weight: 800; text-transform: uppercase; }
    .icon-badge { width: 52px; height: 52px; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #ebf9ee, #d7f1e0); font-size: 1.55rem; }
    .chip { display: inline-block; margin: 0.2rem 0.35rem 0.2rem 0; padding: 0.44rem 0.7rem; border-radius: 999px; background: #edf9f1; color: #194e3a; font-size: 0.76rem; font-weight: 700; }
    .risk-badge { display: inline-flex; align-items: center; justify-content: center; border-radius: 999px; padding: 0.42rem 0.8rem; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
    .risk-low { background: rgba(24,159,87,0.14); color: #1a7d4c; }
    .risk-medium { background: rgba(225,162,24,0.14); color: #a46300; }
    .risk-high { background: rgba(193,57,42,0.14); color: #9b2d22; }
    .value-box { background: #f9fdfb; border: 1px solid #dfeae3; border-radius: 16px; padding: 0.84rem; }
    .value-box strong { display: block; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: #546d62; }
    .value-box span { display: block; margin-top: 0.45rem; font-weight: 800; color: #173d2e; }
    .plain-label { color: #214c3c; font-weight: 800; margin-bottom: 0.6rem; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    div[data-baseweb="input"] input {
        background-color: #ffffff !important;
        color: #17231c !important;
        -webkit-text-fill-color: #17231c !important;
        border-color: #cbd9cf !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #69776e !important;
        -webkit-text-fill-color: #69776e !important;
    }
    [data-baseweb="select"] > div { background-color: #ffffff !important; color: #17231c !important; }
    .profile-form-shell { background: #ffffff; border: 1px solid #dfeae2; border-radius: 20px; padding: 1.3rem; box-shadow: 0 12px 28px rgba(17,59,42,0.05); }
    div.stButton > button { border: 1px solid #d4e4d9; border-radius: 12px; background: linear-gradient(135deg, #ffffff 0%, #edf9f1 100%); color: #173d2e; font-weight: 700; padding: 0.7rem 1rem; }
    div.stButton > button:hover { border-color: #90bb9e; box-shadow: 0 12px 24px rgba(18,110,68,0.1); }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #1c8d56 0%, #0d6d3f 100%); color: white; }
</style>
"""


def t(key):
    language = st.session_state.get("language", "English")
    return TRANSLATIONS.get(language, TRANSLATIONS["English"]).get(key, key)


ANIMAL_LABELS = {
    "Hindi": ["गाय", "भैंस", "बकरी", "भेड़", "मुर्गी", "बत्तख", "सूअर", "कुत्ता", "बिल्ली", "घोड़ा", "गधा", "ऊँट", "खरगोश", "टर्की", "कबूतर"],
    "Kannada": ["ಹಸು", "ಎಮ್ಮೆ", "ಮೇಕೆ", "ಕುರಿ", "ಕೋಳಿ", "ಬಾತುಕೋಳಿ", "ಹಂದಿ", "ನಾಯಿ", "ಬೆಕ್ಕು", "ಕುದುರೆ", "ಕತ್ತೆ", "ಒಂಟೆ", "ಮೊಲ", "ಟರ್ಕಿ", "ಪಾರಿವಾಳ"],
    "Marathi": ["गाय", "म्हैस", "शेळी", "मेंढी", "कोंबडी", "बदक", "डुक्कर", "कुत्रा", "मांजर", "घोडा", "गाढव", "उंट", "ससा", "टर्की", "कबूतर"],
    "Telugu": ["ఆవు", "గేదె", "మేక", "గొర్రె", "కోడి", "బాతు", "పంది", "కుక్క", "పిల్లి", "గుర్రం", "గాడిద", "ఒంటె", "కుందేలు", "టర్కీ", "పావురం"],
    "Tamil": ["பசு", "எருமை", "ஆடு", "செம்மறியாடு", "கோழி", "வாத்து", "பன்றி", "நாய்", "பூனை", "குதிரை", "கழுதை", "ஒட்டகம்", "முயல்", "வான்கோழி", "புறா"],
}
SYMPTOM_LABELS = {
    "Hindi": ["बुखार", "खाँसी", "दस्त", "उल्टी", "खाना नहीं खाना", "कम खाना", "कमज़ोरी", "सुस्ती", "साँस लेने में कठिनाई", "नाक से स्राव", "आँख से स्राव", "सूजन", "त्वचा के घाव", "खुजली", "बाल झड़ना", "घाव", "लंगड़ाना", "पेट में सूजन", "पेट फूलना", "मुँह में घाव", "अधिक लार", "दूध कम होना", "असामान्य दूध", "वजन कम होना", "कब्ज", "कंपकंपी", "दौरे", "खून आना", "अधिक प्यास", "बार-बार पेशाब", "प्रजनन समस्या", "किलनी", "निर्जलीकरण", "असामान्य स्राव"],
    "Kannada": ["ಜ್ವರ", "ಕೆಮ್ಮು", "ಅತಿಸಾರ", "ವಾಂತಿ", "ತಿನ್ನುತ್ತಿಲ್ಲ", "ಕಡಿಮೆ ತಿನ್ನುವುದು", "ದೌರ್ಬಲ್ಯ", "ಆಲಸ್ಯ", "ಉಸಿರಾಟದ ತೊಂದರೆ", "ಮೂಗಿನಿಂದ ಸ್ರಾವ", "ಕಣ್ಣಿನಿಂದ ಸ್ರಾವ", "ಊತ", "ಚರ್ಮದ ಗಾಯಗಳು", "ತುರಿಕೆ", "ಕೂದಲು ಉದುರುವುದು", "ಗಾಯಗಳು", "ಕುಂಟು", "ಹೊಟ್ಟೆ ಊತ", "ಹೊಟ್ಟೆ ಉಬ್ಬುವುದು", "ಬಾಯಿಯ ಗಾಯಗಳು", "ಹೆಚ್ಚಿನ ಲಾಲಾರಸ", "ಹಾಲು ಕಡಿಮೆಯಾಗುವುದು", "ಅಸಹಜ ಹಾಲು", "ತೂಕ ಇಳಿಕೆ", "ಮಲಬದ್ಧತೆ", "ನಡುಕ", "ಸೆಳೆತ", "ರಕ್ತಸ್ರಾವ", "ಹೆಚ್ಚಿನ ದಾಹ", "ಹೆಚ್ಚು ಮೂತ್ರ ವಿಸರ್ಜನೆ", "ಸಂತಾನೋತ್ಪತ್ತಿ ಸಮಸ್ಯೆ", "ಉಣ್ಣಿ", "ನಿರ್ಜಲೀಕರಣ", "ಅಸಹಜ ಸ್ರಾವ"],
    "Marathi": ["ताप", "खोकला", "अतिसार", "उलटी", "खात नाही", "कमी खाणे", "अशक्तपणा", "सुस्ती", "श्वास घेण्यास त्रास", "नाकातून स्राव", "डोळ्यातून स्राव", "सूज", "त्वचेवरील जखमा", "खाज", "केस गळणे", "जखमा", "लंगडणे", "पोटाची सूज", "पोट फुगणे", "तोंडातील जखमा", "जास्त लाळ", "दूध कमी होणे", "असामान्य दूध", "वजन कमी होणे", "बद्धकोष्ठता", "थरथरणे", "झटके", "रक्तस्त्राव", "जास्त तहान", "वारंवार लघवी", "प्रजनन समस्या", "गोचीड", "निर्जलीकरण", "असामान्य स्राव"],
    "Telugu": ["జ్వరం", "దగ్గు", "విరేచనాలు", "వాంతులు", "తినకపోవడం", "తక్కువగా తినడం", "బలహీనత", "నీరసం", "శ్వాస తీసుకోవడంలో ఇబ్బంది", "ముక్కు స్రావం", "కంటి స్రావం", "వాపు", "చర్మ గాయాలు", "దురద", "జుట్టు రాలడం", "గాయాలు", "కుంటడం", "కడుపు వాపు", "కడుపు ఉబ్బరం", "నోటి గాయాలు", "అధిక లాలాజలం", "పాలు తగ్గడం", "అసాధారణ పాలు", "బరువు తగ్గడం", "మలబద్ధకం", "వణుకు", "మూర్ఛలు", "రక్తస్రావం", "అధిక దాహం", "తరచుగా మూత్రం", "పునరుత్పత్తి సమస్య", "పురుగులు", "డీహైడ్రేషన్", "అసాధారణ స్రావం"],
    "Tamil": ["காய்ச்சல்", "இருமல்", "வயிற்றுப்போக்கு", "வாந்தி", "சாப்பிடாமல் இருப்பது", "குறைவாக சாப்பிடுதல்", "பலவீனம்", "சோர்வு", "சுவாசிப்பதில் சிரமம்", "மூக்கில் சுரப்பு", "கண்ணில் சுரப்பு", "வீக்கம்", "தோல் புண்கள்", "அரிப்பு", "முடி உதிர்தல்", "காயங்கள்", "நொண்டுதல்", "வயிற்று வீக்கம்", "வயிறு உப்புசம்", "வாய் புண்கள்", "அதிக உமிழ்நீர்", "பால் உற்பத்தி குறைவு", "அசாதாரண பால்", "எடை குறைதல்", "மலச்சிக்கல்", "நடுக்கம்", "வலிப்பு", "இரத்தப்போக்கு", "அதிக தாகம்", "அடிக்கடி சிறுநீர்", "இனப்பெருக்க பிரச்சினை", "உண்ணிகள்", "நீரிழப்பு", "அசாதாரண சுரப்பு"],
}


def choice_label(value, choices):
    language = st.session_state.get("language", "English")
    labels = choices.get(language)
    values = ANIMAL_OPTIONS if choices is ANIMAL_LABELS else SYMPTOMS
    if labels and value in values:
        return labels[values.index(value)]
    return humanize(value)


def humanize(value):
    if value is None:
        return ""
    return str(value).replace("_", " ").title()


CONDITION_KEYS = {
    "Respiratory illness warning": "respiratory_warning",
    "Digestive illness / dehydration warning": "digestive_warning",
    "Skin or external parasite warning": "skin_warning",
    "Injury or inflammation warning": "injury_warning",
    "General illness / nutrition warning": "general_warning",
    "Milk production / udder health warning": "milk_warning",
    "Neurological warning": "neurological_warning",
    "No specific condition pattern detected": "no_pattern",
}


def localized_condition(value):
    key = CONDITION_KEYS.get(value)
    return t(key) if key else value


def localized_risk_level(value):
    keys = {
        "Critical": "risk_critical",
        "High Concern": "risk_high_concern",
        "Moderate Concern": "risk_moderate_concern",
        "Mild Concern": "risk_mild_concern",
        "High": "high_risk",
        "Medium": "medium_risk",
        "Low": "low_risk",
    }
    return t(keys[value]) if value in keys else value


def localized_care_advice(symptoms, level):
    advice = [t("care_clean_water")]
    if "diarrhea" in symptoms or "vomiting" in symptoms:
        advice.append(t("care_dehydration"))
    if "difficulty_breathing" in symptoms:
        advice.append(t("care_breathing"))
    if "seizures" in symptoms or "bleeding" in symptoms:
        advice.append(t("care_urgent"))
    if "wounds" in symptoms:
        advice.append(t("care_wound"))
    if "ticks" in symptoms:
        advice.append(t("care_ticks"))
    if level in {"High Concern", "Critical"}:
        advice.append(t("care_vet"))
    advice.append(t("care_no_medicine"))
    return " ".join(advice)


def set_widget_selection(key, values):
    st.session_state[key] = list(values)


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_reports():
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM animal_reports ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Data access

def save_profile(full_name, mobile, role, language):
    conn = connect_db()
    existing = conn.execute(
        "SELECT * FROM profiles WHERE mobile = ? AND role = ? LIMIT 1",
        (mobile.strip(), role),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE profiles SET full_name = ?, language = ? WHERE id = ?",
            (full_name.strip(), language, existing["id"]),
        )
        conn.commit()
        result = dict(conn.execute("SELECT * FROM profiles WHERE id = ?", (existing["id"],)).fetchone())
        conn.close()
        return result

    now = datetime.now().isoformat(timespec="seconds")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO profiles (full_name, mobile, role, language, created_at) VALUES (?, ?, ?, ?, ?)",
        (full_name.strip(), mobile.strip(), role, language, now),
    )
    profile_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    conn.commit()
    conn.close()
    return dict(row)


def load_profile_reports(profile_id=None, role=None):
    conn = connect_db()
    if profile_id and role == "Farmer":
        rows = conn.execute("SELECT * FROM animal_reports WHERE profile_id = ? ORDER BY id DESC", (profile_id,)).fetchall()
    elif role in {"Veterinary", "Government"}:
        rows = conn.execute("SELECT * FROM animal_reports ORDER BY id DESC").fetchall()
    elif profile_id:
        rows = conn.execute("SELECT * FROM animal_reports WHERE profile_id = ? ORDER BY id DESC", (profile_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM animal_reports ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_report_entry(profile_id, selected_animals, symptoms, village, days_sick):
    if not selected_animals:
        raise ValueError(t("validation_missing_animals"))
    if not village.strip():
        raise ValueError(t("validation_missing_village"))
    if not symptoms:
        raise ValueError(t("validation_missing_symptoms"))

    score, condition, conditions, care = calculate_risk(symptoms, days_sick)
    risk_level = "Critical" if score >= 70 else "High Concern" if score >= 50 else "Moderate Concern" if score >= 25 else "Mild Concern"
    animal_type = selected_animals[0] if len(selected_animals) == 1 else "Multiple animals"
    now = datetime.now().isoformat(timespec="seconds")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO animal_reports (
            profile_id, animal_type, village, symptoms, days_sick,
            risk_score, risk_level, possible_conditions, care_advice,
            status, is_demo, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            profile_id,
            animal_type,
            village.strip(),
            json.dumps(symptoms),
            int(days_sick),
            int(score),
            risk_level,
            json.dumps(conditions),
            care,
            "Submitted",
            0,
            now,
        ),
    )
    report_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM animal_reports WHERE id = ?", (report_id,)).fetchone()
    conn.commit()
    conn.close()
    return dict(row)


def get_village_summary():
    reports = load_profile_reports()
    village_data = {}
    for report in reports:
        village = (report.get("village") or "").strip()
        if not village:
            continue
        if village not in village_data:
            village_data[village] = {"village": village, "total_reports": 0, "scores": [], "high_risk": 0}
        case = village_data[village]
        case["total_reports"] += 1
        case["scores"].append(report.get("risk_score") or 0)
        if str(report.get("risk_level") or "").lower() in {"high concern", "critical"}:
            case["high_risk"] += 1

    output = []
    for village, item in village_data.items():
        avg = sum(item["scores"]) / len(item["scores"]) if item["scores"] else 0
        risk_score = min(round(avg + min(item["total_reports"] * 5, 25)), 100)
        if risk_score >= 70:
            level = "Critical"
        elif risk_score >= 50:
            level = "High"
        elif risk_score >= 25:
            level = "Medium"
        else:
            level = "Low"
        output.append({
            "village": village,
            "total_reports": item["total_reports"],
            "risk_score": risk_score,
            "risk_level": level,
            "high_risk_cases": item["high_risk"],
        })
    return sorted(output, key=lambda item: item["risk_score"], reverse=True)


def alert_summary():
    alerts = []
    for report in load_profile_reports():
        score = int(report.get("risk_score") or 0)
        if score >= 55:
            alerts.append({
                "village": report.get("village") or "Unknown",
                "animal": report.get("animal_type") or "Unknown",
                "condition": report.get("risk_level") or "Alert",
                "risk_score": score,
            })
    return alerts


def get_dashboard_data():
    reports = load_profile_reports()
    return {
        "total_reports": len(reports),
        "high_risk_cases": sum(1 for item in reports if (item.get("risk_score") or 0) >= 50),
        "medium_risk_cases": sum(1 for item in reports if 25 <= (item.get("risk_score") or 0) < 50),
        "low_risk_cases": sum(1 for item in reports if (item.get("risk_score") or 0) < 25),
        "village_count": len({(item.get("village") or "").strip() for item in reports if (item.get("village") or "").strip()}),
    }


def risk_label(score):
    if score >= 70:
        return "HIGH RISK"
    if score >= 50:
        return "MEDIUM RISK"
    return "LOW RISK"


def badge_class(score):
    if score >= 70:
        return "risk-high"
    if score >= 50:
        return "risk-medium"
    return "risk-low"


def read_aloud_button(label, text, key_name):
    if st.button(label, key=key_name, use_container_width=False):
        st.session_state["speech_text"] = text
        st.rerun()


def speak_text(text, language_name):
    lang_code = LANGUAGE_CODES.get(language_name, "en-IN")
    script = f"""
    <script>
        try {{
            const utterance = new SpeechSynthesisUtterance({json.dumps(text)});
            utterance.lang = '{lang_code}';
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }} catch (error) {{
            console.log('Speech not available');
        }}
    </script>
    """
    components.html(script, height=0)


def render_top_bar():
    st.markdown("<div class='topbar-shell'>", unsafe_allow_html=True)
    cols = st.columns([1.2, 1.5, 0.9])
    with cols[0]:
        st.markdown(f"<div class='tag'>{t('app_name')}</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<div style='text-align:center; font-weight:800; color:#143d2f; font-size:1.05rem;'>{t('subtitle')}</div>", unsafe_allow_html=True)
    with cols[2]:
        selected = st.selectbox(
            t("language_label"),
            options=list(LANGUAGE_CODES.keys()),
            index=list(LANGUAGE_CODES.keys()).index(st.session_state.get("language", "English")),
            label_visibility="collapsed",
            key="language_selector",
        )
        if selected != st.session_state.get("language", "English"):
            st.session_state.language = selected
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_profile_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='hero-shell'>
            <div class='eyebrow'>{t('hero_eyebrow')}</div>
            <h1 class='hero-title'>{t('landing_title')}</h1>
            <div class='hero-subtitle'>{t('subtitle')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='profile-form-shell'>", unsafe_allow_html=True)
    st.markdown(f"<h2>{t('profile_heading')}</h2><p>{t('profile_description')}</p>", unsafe_allow_html=True)
    with st.form("profile_form"):
        full_name = st.text_input(t("full_name"), max_chars=80)
        mobile = st.text_input(t("mobile"), max_chars=15, placeholder="9876543210")
        role = st.selectbox(
            t("choose_portal"),
            options=ROLE_OPTIONS,
            format_func=lambda item: t(item.lower() if item != "Veterinary" else "veterinarian"),
        )
        submitted = st.form_submit_button(t("continue"), type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not full_name.strip() or not mobile.strip():
            st.error(t("profile_required"))
        else:
            profile = save_profile(
                full_name,
                mobile,
                role,
                st.session_state.get("language", "English"),
            )
            st.session_state.profile = profile
            st.session_state.last_report_result = None
            st.session_state.pop("module_report_result", None)
            st.session_state.page = "portals"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('demo_data')} · {t('demo_profiles')}</div>", unsafe_allow_html=True)
    st.caption(t("demo_credentials"))
    demo_profiles = [
        ("Farmer", "demo_farmer", "demo_farmer_name", "9000000001", "🌾"),
        ("Veterinary", "demo_veterinary", "demo_veterinary_name", "9000000002", "🩺"),
        ("Government", "demo_government", "demo_government_name", "9000000003", "🏛️"),
    ]
    demo_columns = st.columns(3)
    for column, (role, title_key, name_key, mobile, icon) in zip(demo_columns, demo_profiles):
        with column:
            st.markdown(
                f"<div class='portal-card'><div class='icon-badge'>{icon}</div><h3>{t(title_key)}</h3><p><strong>{t(name_key)}</strong><br>{mobile}</p></div>",
                unsafe_allow_html=True,
            )
            if st.button(t("use_demo"), key=f"use_demo_{role}", use_container_width=True):
                profile = save_profile(t(name_key), mobile, role, st.session_state.get("language", "English"))
                st.session_state.profile = profile
                st.session_state.last_report_result = None
                st.session_state.pop("module_report_result", None)
                st.session_state.page = "portals"
                st.rerun()

    read_aloud_button(t("read_aloud"), f"{t('landing_title')}. {t('subtitle')}", "profile_read_aloud")


def render_portals_page():
    profile = st.session_state.get("profile")
    if not profile:
        st.session_state.page = "profile"
        st.rerun()

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if st.button(t("back_to_profile"), key="portal_back_to_profile", use_container_width=False):
        st.session_state.page = "profile"
        st.session_state.profile = None
        st.rerun()

    role_key = {"Farmer": "farmer", "Veterinary": "veterinarian", "Government": "government"}[profile["role"]]
    portal_title = t(role_key + "_portal")
    st.markdown(f"<div class='tag'>{t(role_key)}</div><h1 style='margin: 0.8rem 0 0.3rem;'>{portal_title}</h1>", unsafe_allow_html=True)
    st.caption(f"{t('welcome')}, {profile.get('full_name', '')}")
    read_aloud_button(t("read_aloud"), f"{portal_title}. {t('welcome')} {profile.get('full_name', '')}.", "portal_read_aloud")

    modules = PORTAL_MODULES.get(profile["role"], [])
    for start in range(0, len(modules), 3):
        row_modules = modules[start:start + 3]
        columns = st.columns(len(row_modules))
        for column, (module_key, icon, title_key, description_key) in zip(columns, row_modules):
            with column:
                title = t(title_key)
                st.markdown(
                    f"""
                    <div class='portal-card'>
                        <div class='icon-badge'>{icon}</div>
                        <h3>{title}</h3>
                        <p style='margin-top:0.8rem;'>{t(description_key)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(t("open_module").format(title=title), key=f"open_module_{module_key}", use_container_width=True):
                    st.session_state.portal_module = module_key
                    st.session_state.page = "module"
                    st.rerun()


def render_module_page():
    profile = st.session_state.get("profile")
    if not profile:
        st.session_state.page = "profile"
        st.rerun()

    module_key = st.session_state.get("portal_module")
    modules = {item[0]: item for item in PORTAL_MODULES.get(profile["role"], [])}
    module = modules.get(module_key)
    if not module:
        st.session_state.page = "portals"
        st.rerun()

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if st.button(f"← {t('back_modules')}", key="module_back", use_container_width=False):
        st.session_state.page = "portals"
        st.rerun()
    role_key = {"Farmer": "farmer", "Veterinary": "veterinarian", "Government": "government"}[profile["role"]]
    st.markdown(f"<div class='tag'>{t(role_key)}</div><h1 style='margin: 0.8rem 0 0.3rem;'>{t(module[2])}</h1>", unsafe_allow_html=True)
    st.caption(t("role_caption").format(name=profile.get("full_name", ""), role=t(role_key)))
    read_aloud_button(t("read_aloud"), f"{t(module[2])}. {t(module[3])}.", f"module_read_aloud_{module_key}")

    if module_key == "health":
        animal_actions = st.columns(2)
        animal_actions[0].button(
            t("select_all"),
            key="select_all_module_animals",
            on_click=set_widget_selection,
            args=("module_animals", ANIMAL_OPTIONS),
        )
        animal_actions[1].button(
            t("clear_selection"),
            key="clear_module_animals",
            on_click=set_widget_selection,
            args=("module_animals", []),
        )
        animals = st.multiselect(
            t("animal_type"),
            ANIMAL_OPTIONS,
            format_func=lambda item: choice_label(item, ANIMAL_LABELS),
            key="module_animals",
            select_all=False,
        )
        symptom_actions = st.columns(2)
        symptom_actions[0].button(
            t("select_all"),
            key="select_all_module_symptoms",
            on_click=set_widget_selection,
            args=("module_symptoms", SYMPTOMS),
        )
        symptom_actions[1].button(
            t("clear_selection"),
            key="clear_module_symptoms",
            on_click=set_widget_selection,
            args=("module_symptoms", []),
        )
        symptoms = st.multiselect(
            t("symptoms"),
            SYMPTOMS,
            format_func=lambda item: choice_label(item, SYMPTOM_LABELS),
            key="module_symptoms",
            select_all=False,
        )
        with st.form("module_health_report"):
            village = st.text_input(t("village"), key="module_village")
            days_sick = st.number_input(t("days_sick"), min_value=0, max_value=365, value=1, key="module_days_sick")
            submitted = st.form_submit_button(t("submit_report"), type="primary")
        if submitted:
            try:
                result = create_report_entry(profile["id"], animals, symptoms, village, int(days_sick))
                st.session_state.module_report_result = result
                st.success(t("submit_success"))
            except ValueError as exc:
                st.error(str(exc))
        result = st.session_state.get("module_report_result")
        if result:
            st.metric(t("risk_score"), f"{result['risk_score']}/100", localized_risk_level(result["risk_level"]))
            conditions = json.loads(result.get("possible_conditions") or "[]")
            symptoms = json.loads(result.get("symptoms") or "[]")
            st.write(f"**{t('possible_conditions')}:** {' | '.join(localized_condition(item) for item in conditions)}")
            st.write(f"**{t('health_advice')}:** {localized_care_advice(symptoms, result['risk_level'])}")
            st.caption(t("disclaimer"))
    elif module_key in {"reports", "animal_reports"}:
        reports = load_profile_reports(
            profile_id=profile["id"] if profile["role"] == "Farmer" else None,
            role=profile["role"],
        )
        if reports:
            for report in reports:
                symptoms = json.loads(report.get("symptoms") or "[]")
                risk_score = int(report.get("risk_score") or 0)
                st.markdown(
                    f"<div class='portal-card'><div class='risk-badge {badge_class(risk_score)}'>{t('high_risk') if risk_score >= 50 else t('low_risk')}</div><h3>{choice_label(report.get('animal_type', 'Animal'), ANIMAL_LABELS)} · {report.get('village', '')}</h3><p>{t('risk_score')}: {risk_score}/100 · {report.get('created_at', '')}</p><p>{t('symptoms')}: {', '.join(choice_label(item, SYMPTOM_LABELS) for item in symptoms)}</p><p>{localized_care_advice(symptoms, report.get('risk_level', ''))}</p></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info(t("no_reports"))
    elif module_key == "appointments":
        with st.form("module_appointment"):
            appointment_date = st.date_input(t("appointment_date"))
            appointment_time = st.time_input(t("appointment_time"))
            reason = st.text_area(t("reason"))
            submitted = st.form_submit_button(t("request_appointment"), type="primary")
        if submitted:
            if not reason.strip():
                st.error(t("enter_reason"))
            else:
                conn = connect_db()
                conn.execute(
                    "INSERT INTO appointments (farmer_profile_id, appointment_date, appointment_time, reason, status, is_demo, created_at) VALUES (?, ?, ?, ?, 'Pending', 0, ?)",
                    (profile["id"], appointment_date.isoformat(), appointment_time.strftime("%H:%M"), reason.strip(), datetime.now().isoformat(timespec="seconds")),
                )
                conn.commit()
                conn.close()
                st.success(t("appointment_success"))
        conn = connect_db()
        rows = conn.execute("SELECT * FROM appointments WHERE farmer_profile_id = ? ORDER BY id DESC", (profile["id"],)).fetchall()
        conn.close()
        if rows:
            st.dataframe(
                [{t("appointment_date"): row["appointment_date"], t("appointment_time"): row["appointment_time"], t("reason"): row["reason"], t("status_label"): t("status_" + row["status"].lower()) if row["status"].lower() in {"pending", "approved", "rejected"} else row["status"]} for row in rows],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(t("no_appointments"))
    elif module_key == "appointment_requests":
        conn = connect_db()
        rows = conn.execute("SELECT * FROM appointments ORDER BY id DESC").fetchall()
        conn.close()
        if rows:
            st.dataframe(
                [{t("appointment_date"): row["appointment_date"], t("appointment_time"): row["appointment_time"], t("reason"): row["reason"], t("status_label"): t("status_" + row["status"].lower()) if row["status"].lower() in {"pending", "approved", "rejected"} else row["status"]} for row in rows],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(t("no_appointment_requests"))
    elif module_key == "laboratory":
        conn = connect_db()
        rows = conn.execute("SELECT * FROM lab_reports ORDER BY id DESC").fetchall()
        conn.close()
        if rows:
            st.dataframe(
                [{t("reported_animal"): row["report_id"], t("lab_result"): row["result"], t("medicine"): row["medicine"], t("follow_up"): t("yes") if row["follow_up_required"] else t("no"), t("notes"): row["notes"]} for row in rows],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(t("no_laboratory_records"))
    elif module_key == "village_risk":
        summary = get_village_summary()
        if summary:
            st.bar_chart(pd.DataFrame(summary).set_index("village")["risk_score"], height=240)
            st.dataframe(
                [{t("village"): row["village"], t("total_reports"): row["total_reports"], t("risk_score"): row["risk_score"], t("risk_level"): localized_risk_level(row["risk_level"])} for row in summary],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(t("no_reports"))
    elif module_key in {"notifications", "risk_management"}:
        alerts = alert_summary()
        if alerts:
            st.dataframe(
                [{t("village"): row["village"], t("reported_animal"): row["animal"], t("health_condition"): localized_risk_level(row["condition"]), t("risk_score"): row["risk_score"]} for row in alerts],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(t("no_alerts"))
    elif module_key == "care":
        st.markdown(f"<h2>{t('care_guide_title')}</h2>", unsafe_allow_html=True)
        animal = st.selectbox(
            t("care_choose_animal"),
            options=ANIMAL_OPTIONS,
            format_func=lambda item: choice_label(item, ANIMAL_LABELS),
            key="care_animal",
        )
        care_group = CARE_GROUP_BY_ANIMAL[animal]
        topic = st.selectbox(
            t("care_choose_topic"),
            options=CARE_TOPICS_BY_GROUP[care_group],
            format_func=lambda item: t(CARE_TOPIC_TITLE_KEYS[item]),
            key="care_topic",
        )
        st.markdown(f"### {t(CARE_TOPIC_TITLE_KEYS[topic])}")
        st.markdown(f"**{t('care_supportive_label')}:** {localized_care_advice(CARE_TOPIC_SYMPTOMS[topic], 'High Concern')}")
        st.warning(f"**{t('care_urgent_label')}:** {t('care_urgent_signs')}")
        st.info(t("care_group_" + care_group))
        st.caption(t("care_no_treatment"))
        st.caption(t("care_scope_note"))


def render_farmer_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if st.button(t("back_to_profile"), key="farmer_back_to_profile", use_container_width=False):
        st.session_state.page = "profile"
        st.rerun()

    profile = st.session_state.get("profile")
    if not profile:
        st.session_state.page = "profile"
        st.rerun()

    st.markdown(f"<div class='tag'>{t('farmer_portal')}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='margin: 0.8rem 0 0.6rem;'>{t('farmer_portal')}</h1>", unsafe_allow_html=True)
    st.caption(f"{t('welcome')}, {profile.get('full_name', 'Farmer')}")

    stats = get_dashboard_data()
    metric_cols = st.columns(4)
    metric_cols[0].metric(t("total_reports"), stats["total_reports"])
    metric_cols[1].metric(t("high_risk_cases"), stats["high_risk_cases"])
    metric_cols[2].metric(t("medium_risk_cases"), stats["medium_risk_cases"])
    metric_cols[3].metric(t("low_risk_cases"), stats["low_risk_cases"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('animal_health_report')}</div>", unsafe_allow_html=True)

    with st.form("farmer_form"):
        selected_animals = st.multiselect(
            t("animal_selection"),
            options=ANIMAL_OPTIONS,
            default=st.session_state.get("selected_animals", []),
        )
        village = st.text_input(t("village"), value=st.session_state.get("farmer_village", ""))
        days_sick = st.number_input(t("days_sick"), min_value=0, max_value=365, value=st.session_state.get("days_sick", 2))
        symptoms = st.multiselect(
            t("symptoms"),
            options=SYMPTOMS,
            default=st.session_state.get("selected_symptoms", []),
            format_func=humanize,
        )
        st.session_state.selected_animals = selected_animals
        st.session_state.selected_symptoms = symptoms
        st.session_state.farmer_village = village
        st.session_state.days_sick = int(days_sick)
        submitted = st.form_submit_button(t("submit_report"), type="primary")

    if submitted:
        try:
            result = create_report_entry(profile["id"], selected_animals, symptoms, village, int(days_sick))
            st.session_state.last_report_result = result
            st.session_state.selected_animals = []
            st.session_state.selected_symptoms = []
            st.success(t("submit_success"))
        except ValueError as exc:
            st.error(str(exc))

    if st.session_state.get("last_report_result"):
        result = st.session_state["last_report_result"]
        score = int(result.get("risk_score") or 0)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='report-card'>
                <div class='tag'>{t('health_condition')}</div>
                <h3 style='margin: 0.9rem 0 0.4rem;'>{result.get('risk_level', '')}</h3>
                <div class='risk-badge {badge_class(score)}'>{risk_label(score)}</div>
                <p style='margin-top:1rem; color:#5d7369;'>{t('disclaimer')}</p>
                <div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:0.8rem; margin-top:1rem;'>
                    <div class='value-box'><strong>{t('risk_score')}</strong><span>{score}/100</span></div>
                    <div class='value-box'><strong>{t('reported_animal')}</strong><span>{result.get('animal_type', '')}</span></div>
                    <div class='value-box'><strong>{t('village')}</strong><span>{result.get('village', '')}</span></div>
                    <div class='value-box'><strong>{t('time')}</strong><span>{result.get('created_at', '')}</span></div>
                </div>
                <div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:0.8rem; margin-top:0.9rem;'>
                    <div class='value-box'><strong>{t('health_advice')}</strong><span>{result.get('care_advice', '')}</span></div>
                    <div class='value-box'><strong>{t('possible_conditions')}</strong><span>{' | '.join(json.loads(result.get('possible_conditions') or '[]'))}</span></div>
                    <div class='value-box'><strong>{t('disease_risk_prediction')}</strong><span>{result.get('risk_level', '')}</span></div>
                </div>
                <div style='margin-top:1rem;'><div class='plain-label'>{t('detected_symptoms')}</div></div>
                <div>{' '.join(f'<span class="chip">{humanize(item)}</span>' for item in (json.loads(result.get('symptoms') or '[]')))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(t("report_another"), key="farmer_report_another", use_container_width=True):
            st.session_state.last_report_result = None
            st.session_state.selected_animals = []
            st.session_state.selected_symptoms = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('village_health')}</div>", unsafe_allow_html=True)
    summary = get_village_summary()
    if summary:
        df = pd.DataFrame(summary)
        st.bar_chart(df.set_index("village")["risk_score"], height=180)
        for item in summary[:3]:
            st.markdown(
                f"<div class='portal-card'><strong>{item['village']}</strong><br>{t('total_reports')}: {item['total_reports']}<br>{t('risk_score')}: {item['risk_score']}<br>{t('risk_level')}: {item['risk_level']}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info(t("no_reports"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('health_alerts')}</div>", unsafe_allow_html=True)
    alerts = alert_summary()
    if alerts:
        for alert in alerts[:5]:
            st.markdown(
                f"<div class='portal-card'><strong>{alert['village']}</strong><br>{alert['animal']}<br>{alert['condition']}<br>{t('risk_score')}: {alert['risk_score']}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info(t("no_alerts"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('previous_reports')}</div>", unsafe_allow_html=True)
    farmer_reports = load_profile_reports(profile_id=profile["id"], role="Farmer")
    if farmer_reports:
        for report in farmer_reports[:5]:
            risk = int(report.get("risk_score") or 0)
            symptoms_list = json.loads(report.get("symptoms") or "[]")
            st.markdown(
                f"<div class='portal-card'><div class='risk-badge {badge_class(risk)}'>{risk_label(risk)}</div><h4>{report.get('animal_type', 'Animal')}</h4><p>{t('village')}: {report.get('village', '')}<br>{t('symptoms')}: {', '.join(humanize(item) for item in symptoms_list)}</p></div>",
                unsafe_allow_html=True,
            )
    else:
        st.info(t("no_reports"))

    read_aloud_button(t("read_aloud"), f"Farmer portal. {t('animal_health_report')}. {t('village_health')}. {t('health_alerts')}.", "farmer_read_aloud")


def render_veterinarian_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if st.button(t("back_to_profile"), key="vet_back_to_profile", use_container_width=False):
        st.session_state.page = "profile"
        st.rerun()

    st.markdown(f"<div class='tag'>{t('veterinarian_portal')}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='margin: 0.8rem 0 0.6rem;'>{t('veterinarian_portal')}</h1>", unsafe_allow_html=True)

    stats = get_dashboard_data()
    metric_cols = st.columns(4)
    metric_cols[0].metric(t("total_reports"), stats["total_reports"])
    metric_cols[1].metric(t("high_risk_cases"), stats["high_risk_cases"])
    metric_cols[2].metric(t("medium_risk_cases"), stats["medium_risk_cases"])
    metric_cols[3].metric(t("low_risk_cases"), stats["low_risk_cases"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('recent_reports')}</div>", unsafe_allow_html=True)
    reports = load_profile_reports(role="Veterinary")
    if reports:
        for report in reports[:8]:
            risk = int(report.get("risk_score") or 0)
            symptoms_list = json.loads(report.get("symptoms") or "[]")
            st.markdown(
                f"""
                <div class='portal-card'>
                    <div class='risk-badge {badge_class(risk)}'>{risk_label(risk)}</div>
                    <h4 style='margin-top:0.8rem;'>{report.get('animal_type', 'Animal')} · {report.get('village', '')}</h4>
                    <p><strong>{t('risk_score')}:</strong> {risk}/100</p>
                    <p><strong>{t('symptoms')}:</strong> {', '.join(humanize(item) for item in symptoms_list)}</p>
                    <p><strong>{t('possible_conditions')}:</strong> {' | '.join(json.loads(report.get('possible_conditions') or '[]'))}</p>
                    <p><strong>{t('health_advice')}:</strong> {report.get('care_advice', '')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Respond · #{report.get('id')}", key=f"respond_case_{report.get('id')}", use_container_width=True):
                st.session_state.selected_case = report
            if st.session_state.get("selected_case") and st.session_state["selected_case"].get("id") == report.get("id"):
                st.text_area(t("response_note"), value="Veterinary review recommended.", key=f"vet_note_{report.get('id')}")
                if st.button(t("save_response"), key=f"save_response_{report.get('id')}"):
                    st.success(t("completed"))
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info(t("no_reports"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('alert_summary')}</div>", unsafe_allow_html=True)
    alerts = alert_summary()
    if alerts:
        for alert in alerts[:5]:
            st.markdown(
                f"<div class='portal-card'><strong>{alert['village']}</strong><br>{alert['animal']}<br>{alert['condition']}<br>{t('risk_score')}: {alert['risk_score']}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info(t("no_alerts"))

    read_aloud_button(t("read_aloud"), f"Veterinarian portal. {t('recent_reports')}. {t('alert_summary')}.", "vet_read_aloud")


def render_government_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if st.button(t("back_to_profile"), key="gov_back_to_profile", use_container_width=False):
        st.session_state.page = "profile"
        st.rerun()

    st.markdown(f"<div class='tag'>{t('government_portal')}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='margin: 0.8rem 0 0.6rem;'>{t('government_portal')}</h1>", unsafe_allow_html=True)

    stats = get_dashboard_data()
    metric_cols = st.columns(5)
    metric_cols[0].metric(t("total_reports"), stats["total_reports"])
    metric_cols[1].metric(t("total_villages"), stats["village_count"])
    metric_cols[2].metric(t("high_risk_cases"), stats["high_risk_cases"])
    metric_cols[3].metric(t("medium_risk_cases"), stats["medium_risk_cases"])
    metric_cols[4].metric(t("low_risk_cases"), stats["low_risk_cases"])

    st.markdown("<br>", unsafe_allow_html=True)
    summary = get_village_summary()
    if summary:
        st.markdown(f"<div class='plain-label'>{t('village_risk')}</div>", unsafe_allow_html=True)
        df = pd.DataFrame(summary)
        st.bar_chart(df.set_index("village")["risk_score"], height=200)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('alert_summary')}</div>", unsafe_allow_html=True)
    alerts = alert_summary()
    if alerts:
        for alert in alerts[:6]:
            st.markdown(
                f"<div class='portal-card'><strong>{alert['village']}</strong><br>{alert['animal']}<br>{alert['condition']}<br>{t('risk_score')}: {alert['risk_score']}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info(t("no_alerts"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='plain-label'>{t('village_summary')}</div>", unsafe_allow_html=True)
    for item in (summary[:5] if summary else []):
        st.markdown(
            f"<div class='portal-card'><strong>{item['village']}</strong><br>{t('total_reports')}: {item['total_reports']}<br>{t('risk_score')}: {item['risk_score']}<br>{t('risk_level')}: {item['risk_level']}</div>",
            unsafe_allow_html=True,
        )

    read_aloud_button(t("read_aloud"), f"Government portal. {t('village_risk')}. {t('alert_summary')}. {t('village_summary')}.", "gov_read_aloud")


st.set_page_config(page_title="PashuRaksha", page_icon="🐄", layout="wide")

if "language" not in st.session_state:
    st.session_state.language = "English"
if "page" not in st.session_state:
    st.session_state.page = "profile"
if "profile" not in st.session_state:
    st.session_state.profile = None
if "selected_animals" not in st.session_state:
    st.session_state.selected_animals = []
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "last_report_result" not in st.session_state:
    st.session_state.last_report_result = None

# Create the shared schema without inserting demo users or reports.
init_db(seed_demo=False)
render_top_bar()

if "speech_text" in st.session_state:
    speak_text(st.session_state["speech_text"], st.session_state.get("language", "English"))
    st.session_state.pop("speech_text", None)

if st.session_state.page == "profile":
    render_profile_page()
elif st.session_state.page == "portals":
    render_portals_page()
elif st.session_state.page == "module":
    render_module_page()
else:
    st.session_state.page = "portals" if st.session_state.profile else "profile"
    st.rerun()
