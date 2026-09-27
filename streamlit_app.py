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
        "app_name": "PashuRaksha",
        "subtitle": "Livestock Health & Safety",
        "landing_title": "Protecting Livestock. Protecting Communities.",
        "welcome": "Welcome",
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
        "app_name": "पशुरक्षा",
        "subtitle": "पशुधन स्वास्थ्य और सुरक्षा",
        "landing_title": "पशुओं की रक्षा। समुदायों की रक्षा।",
        "welcome": "स्वागत",
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
        "app_name": "ಪಶುರಕ್ಷಾ",
        "subtitle": "ಪಶು ಆರೋಗ್ಯ ಮತ್ತು ಸುರಕ್ಷತೆ",
        "landing_title": "ಪಶುಗಳನ್ನು ರಕ್ಷಿಸಿ. ಸಮುದಾಯಗಳನ್ನು ರಕ್ಷಿಸಿ.",
        "welcome": "ಸ್ವಾಗತ",
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
        "app_name": "पशुरक्षा",
        "subtitle": "पशुधन आरोग्य आणि सुरक्षा",
        "landing_title": "पशूंची संरक्षण. समुदायांची संरक्षण.",
        "welcome": "स्वागत",
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
        "app_name": "పశురక్షా",
        "subtitle": "పశు ఆరోగ్య మరియు భద్రత",
        "landing_title": "పశువులను రక్షించండి. కమ్యూనిటీలను రక్షించండి.",
        "welcome": "స్వాగతం",
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
        "app_name": "பசுரக்ஷா",
        "subtitle": "கால்நடை ஆரோக்கியம் மற்றும் பாதுகாப்பு",
        "landing_title": "கால்நடைகளைப் பாதுகாத்து. சமூகங்களைப் பாதுகாத்து.",
        "welcome": "வரவேற்கிறோம்",
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

CUSTOM_CSS = """
<style>
    #MainMenu, header, footer { display: none !important; }
    .stApp { background: linear-gradient(135deg, #f9fbfa 0%, #edf8f2 100%); }
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
    div.stButton > button { border: 1px solid #d4e4d9; border-radius: 12px; background: linear-gradient(135deg, #ffffff 0%, #edf9f1 100%); color: #173d2e; font-weight: 700; padding: 0.7rem 1rem; }
    div.stButton > button:hover { border-color: #90bb9e; box-shadow: 0 12px 24px rgba(18,110,68,0.1); }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #1c8d56 0%, #0d6d3f 100%); color: white; }
</style>
"""


def t(key):
    language = st.session_state.get("language", "English")
    return TRANSLATIONS.get(language, TRANSLATIONS["English"]).get(key, key)


def humanize(value):
    if value is None:
        return ""
    return str(value).replace("_", " ").title()


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
        result = dict(existing)
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
            "Language",
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
        """
        <div class='hero-shell'>
            <div class='eyebrow'>Smart Livestock Health Monitoring</div>
            <h1 class='hero-title'>Protecting Livestock. Protecting Communities.</h1>
            <div class='hero-subtitle'>Livestock Health & Safety</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    cards = [
        ("Farmer", "Demo Farmer", "9000000001", "Report sick animals and check village health"),
        ("Veterinary", "Demo Veterinary", "9000000002", "Manage cases and respond to health alerts"),
        ("Government", "Demo Government", "9000000003", "Monitor villages, risks and livestock health information"),
    ]

    columns = st.columns(3)
    for index, (role, name, mobile, description) in enumerate(cards):
        with columns[index]:
            st.markdown(
                f"""
                <div class='feature-card'>
                    <div class='tag'>{role}</div>
                    <h3>{name}</h3>
                    <p style='font-weight:700; color:#1b4a39; margin-top:0.5rem;'>{mobile}</p>
                    <p style='margin-top:0.9rem;'>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select {role}", key=f"profile_select_{role}", use_container_width=True):
                profile = save_profile(name, mobile, role, st.session_state.get("language", "English"))
                st.session_state.profile = profile
                st.session_state.page = "portals"
                st.rerun()

    read_aloud_button(t("read_aloud"), "Protecting Livestock. Protecting Communities. Livestock Health and Safety.", "profile_read_aloud")


def render_portals_page():
    if not st.session_state.get("profile"):
        st.session_state.page = "profile"
        st.rerun()

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if st.button(t("back_to_profile"), key="portal_back_to_profile", use_container_width=False):
        st.session_state.page = "profile"
        st.rerun()

    st.markdown(f"<h1 style='margin: 1rem 0 0.6rem;'>{t('choose_portal')}</h1>", unsafe_allow_html=True)

    portals = [
        ("Farmer", t("farmer_desc"), "🌾"),
        ("Veterinary", t("veterinarian_desc"), "🩺"),
        ("Government", t("government_desc"), "🏛️"),
    ]
    columns = st.columns(3)
    for index, (portal_name, description, icon) in enumerate(portals):
        with columns[index]:
            st.markdown(
                f"""
                <div class='portal-card'>
                    <div class='icon-badge'>{icon}</div>
                    <h3>{t(portal_name.lower() + '_portal')}</h3>
                    <p style='margin-top:0.8rem;'>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {portal_name} Portal", key=f"open_{portal_name.lower()}_portal", use_container_width=True):
                st.session_state.page = portal_name.lower()
                st.rerun()


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

# Ensure backend demo database is initialized before UI loads.
init_db()
render_top_bar()

if "speech_text" in st.session_state:
    speak_text(st.session_state["speech_text"], st.session_state.get("language", "English"))
    st.session_state.pop("speech_text", None)

if st.session_state.page == "profile":
    render_profile_page()
elif st.session_state.page == "portals":
    render_portals_page()
elif st.session_state.page == "farmer":
    render_farmer_page()
elif st.session_state.page == "veterinarian":
    render_veterinarian_page()
elif st.session_state.page == "government":
    render_government_page()
else:
    render_profile_page()
