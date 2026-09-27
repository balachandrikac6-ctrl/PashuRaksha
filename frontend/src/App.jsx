import React from "react";

const API =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


// =========================================================
// TRANSLATIONS
// =========================================================

const translations = {

  English: {

    appName: "PashuRaksha",
    tagline: "Smart Livestock Health & Veterinary Support",

    profile: "Profile",
    fullName: "Full Name",
    mobile: "Mobile Number",
    role: "Role",
    language: "Language",
    save: "Save & Continue",

    farmer: "Farmer",
    veterinary: "Veterinary",
    government: "Government",

    farmerPortal: "Farmer Portal",
    veterinaryPortal: "Veterinary Portal",
    governmentPortal: "Government Portal",

    welcome: "Welcome",
    backProfile: "Back to Profile",
    readAloud: "🔊 Read Aloud",

    animalHealth: "Animal Health Check",
    animalHealthDesc:
      "Check livestock health risk using reported symptoms.",

    appointments: "Appointments",
    appointmentsDesc:
      "Book and track veterinary appointments.",

    reports: "My Reports",
    reportsDesc:
      "View all animal health reports you submitted.",

    notifications: "Notifications",
    notificationsDesc:
      "View important health and appointment updates.",

    animalCare: "Animal Care",
    animalCareDesc:
      "Learn about common livestock health problems and care.",

    animalReports: "Animal Reports",
    animalReportsDesc:
      "Review livestock health reports submitted by farmers.",

    appointmentRequests: "Appointment Requests",
    appointmentRequestsDesc:
      "Review and manage farmer veterinary requests.",

    laboratory: "Laboratory",
    laboratoryDesc:
      "Add veterinary examination and laboratory results.",

    villageRisk: "Village Risk",
    villageRiskDesc:
      "Monitor animal health risk across villages.",

    riskManagement: "Risk Management",
    riskManagementDesc:
      "Monitor risk levels and plan interventions.",

    checkHealth: "Check Animal Health",
    animalType: "Animal Type",
    village: "Village Name",
    symptoms: "Symptoms",
    daysSick: "Number of Days Suffering",
    submit: "Submit Report",

    selectAnimal: "Select animal",
    enterVillage: "Enter village name",
    selectSymptoms: "Select all symptoms you observe",

    riskResult: "Health Risk Result",
    riskScore: "Risk Score",
    riskLevel: "Risk Level",
    possibleConditions: "Possible Warning Patterns",
    careAdvice: "Care Recommendations",

    critical: "Critical",
    high: "High Concern",
    moderate: "Moderate Concern",
    mild: "Mild Concern",
    noRisk: "No Significant Risk",

    totalReports: "Total Reports",
    highCases: "High Risk Cases",
    lowCases: "Lower Risk Cases",

    noReports: "No reports available.",
    noAppointments: "No appointments available.",
    noNotifications: "No notifications available.",

    bookAppointment: "Book Appointment",
    appointmentDate: "Appointment Date",
    appointmentTime: "Appointment Time",
    reason: "Reason",
    book: "Book Appointment",

    pending: "Pending",
    approved: "Approved",
    rejected: "Rejected",
    completed: "Completed",

    accept: "Approve",
    reject: "Reject",
    view: "View",

    labResult: "Laboratory / Examination Result",
    medicine: "Veterinary Medicine / Instructions",
    followUp: "Follow-up Required",
    followUpDate: "Follow-up Date",
    notes: "Veterinary Notes",
    saveLab: "Save Report",

    normal: "Normal",
    needsAttention: "Needs Attention",

    animalCareTitle: "Livestock Care Guide",
    supportiveCare: "Supportive Care",
    veterinaryCare: "Veterinary Care",

    villageRiskTitle: "Village Health Risk",
    animalCount: "Animal Reports",
    averageRisk: "Risk Score",

    riskManagementTitle: "Risk Management",
    monitor: "Monitor",
    action: "Suggested Action",

    low: "Low",
    medium: "Medium",
    high: "High",

    successProfile: "Profile saved successfully.",
    successReport: "Health report submitted successfully.",
    successAppointment: "Appointment request submitted.",
    successLab: "Laboratory report saved successfully.",

    error: "Something went wrong.",
    loading: "Loading...",

    demoData: "Demo Data",
    demoProfiles: "Demo Profiles",
    useDemo: "Use Demo",

    farmerDemo: "Farmer Demo",
    vetDemo: "Veterinary Demo",
    governmentDemo: "Government Demo",

    demoCredentials:
      "Demo profile credentials",

    demoFarmerDetails:
      "Demo Farmer • 9000000001",

    demoVetDetails:
      "Demo Veterinary • 9000000002",

    demoGovernmentDetails:
      "Demo Government • 9000000003",

    respiratoryWarning:
      "Respiratory illness warning",

    digestiveWarning:
      "Digestive illness / dehydration warning",

    skinWarning:
      "Skin or external parasite warning",

    injuryWarning:
      "Injury or inflammation warning",

    generalWarning:
      "General illness / nutrition warning",

    milkWarning:
      "Milk production / udder health warning",

    neurologicalWarning:
      "Neurological warning",

    cleanWater:
      "Provide clean drinking water and keep the animal comfortable.",

    vetRecommended:
      "Veterinary examination is recommended.",

    urgentVet:
      "Seek veterinary care promptly.",

    noPrescription:
      "Do not give prescription medicines without veterinary guidance.",

    cow: "Cow",
    buffalo: "Buffalo",
    goat: "Goat",
    sheep: "Sheep",
    chicken: "Chicken",
    duck: "Duck",
    pig: "Pig",
    dog: "Dog",
    cat: "Cat",
    horse: "Horse",
    donkey: "Donkey",
    camel: "Camel",
    rabbit: "Rabbit",
    turkey: "Turkey",
    pigeon: "Pigeon",

    fever: "Fever",
    cough: "Cough",
    diarrhea: "Diarrhea",
    vomiting: "Vomiting",
    not_eating: "Not eating",
    reduced_eating: "Reduced eating",
    weakness: "Weakness",
    lethargy: "Lethargy",
    difficulty_breathing: "Difficulty breathing",
    nasal_discharge: "Nasal discharge",
    eye_discharge: "Eye discharge",
    swelling: "Swelling",
    skin_lesions: "Skin lesions",
    itching: "Itching",
    hair_loss: "Hair loss",
    wounds: "Wounds",
    lameness: "Lameness",
    abdominal_swelling: "Abdominal swelling",
    bloating: "Bloating",
    mouth_sores: "Mouth sores",
    excessive_salivation: "Excessive salivation",
    milk_drop: "Reduced milk production",
    abnormal_milk: "Abnormal milk",
    weight_loss: "Weight loss",
    constipation: "Constipation",
    tremors: "Tremors",
    seizures: "Seizures",
    bleeding: "Bleeding",
    high_thirst: "Increased thirst",
    frequent_urination: "Frequent urination",
    reproductive_problem: "Reproductive problem",
    ticks: "Ticks",
    dehydration: "Dehydration",
    discharge: "Unusual discharge"
  },


  Kannada: {

    appName: "ಪಶುರಕ್ಷಾ",
    tagline: "ಸ್ಮಾರ್ಟ್ ಪಶು ಆರೋಗ್ಯ ಮತ್ತು ಪಶುವೈದ್ಯಕೀಯ ಸಹಾಯ",

    profile: "ಪ್ರೊಫೈಲ್",
    fullName: "ಪೂರ್ಣ ಹೆಸರು",
    mobile: "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
    role: "ಪಾತ್ರ",
    language: "ಭಾಷೆ",
    save: "ಉಳಿಸಿ ಮತ್ತು ಮುಂದುವರಿಯಿರಿ",

    farmer: "ರೈತ",
    veterinary: "ಪಶುವೈದ್ಯ",
    government: "ಸರ್ಕಾರ",

    farmerPortal: "ರೈತ ಪೋರ್ಟಲ್",
    veterinaryPortal: "ಪಶುವೈದ್ಯ ಪೋರ್ಟಲ್",
    governmentPortal: "ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್",

    welcome: "ಸ್ವಾಗತ",
    backProfile: "ಪ್ರೊಫೈಲ್‌ಗೆ ಹಿಂತಿರುಗಿ",
    readAloud: "🔊 ಓದಿ ಕೇಳಿಸಿ",

    animalHealth: "ಪಶು ಆರೋಗ್ಯ ಪರಿಶೀಲನೆ",
    animalHealthDesc: "ಲಕ್ಷಣಗಳ ಆಧಾರದ ಮೇಲೆ ಪಶು ಆರೋಗ್ಯ ಅಪಾಯ ಪರಿಶೀಲಿಸಿ.",

    appointments: "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳು",
    appointmentsDesc: "ಪಶುವೈದ್ಯಕೀಯ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಬುಕ್ ಮಾಡಿ.",

    reports: "ನನ್ನ ವರದಿಗಳು",
    reportsDesc: "ನೀವು ಸಲ್ಲಿಸಿದ ಎಲ್ಲಾ ಆರೋಗ್ಯ ವರದಿಗಳನ್ನು ನೋಡಿ.",

    notifications: "ಅಧಿಸೂಚನೆಗಳು",
    notificationsDesc: "ಆರೋಗ್ಯ ಮತ್ತು ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ನವೀಕರಣಗಳನ್ನು ನೋಡಿ.",

    animalCare: "ಪಶು ಆರೈಕೆ",
    animalCareDesc: "ಸಾಮಾನ್ಯ ಪಶು ಆರೋಗ್ಯ ಸಮಸ್ಯೆಗಳು ಮತ್ತು ಆರೈಕೆಯನ್ನು ತಿಳಿಯಿರಿ.",

    animalReports: "ಪಶು ವರದಿಗಳು",
    animalReportsDesc: "ರೈತರು ಸಲ್ಲಿಸಿದ ಪಶು ವರದಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",

    appointmentRequests: "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿಗಳು",
    appointmentRequestsDesc: "ರೈತರ ಪಶುವೈದ್ಯಕೀಯ ವಿನಂತಿಗಳನ್ನು ನಿರ್ವಹಿಸಿ.",

    laboratory: "ಪ್ರಯೋಗಾಲಯ",
    laboratoryDesc: "ಪಶುವೈದ್ಯಕೀಯ ಪರೀಕ್ಷೆ ಮತ್ತು ಪ್ರಯೋಗಾಲಯ ಫಲಿತಾಂಶ ಸೇರಿಸಿ.",

    villageRisk: "ಗ್ರಾಮದ ಅಪಾಯ",
    villageRiskDesc: "ಗ್ರಾಮಗಳಲ್ಲಿನ ಪಶು ಆರೋಗ್ಯ ಅಪಾಯವನ್ನು ಗಮನಿಸಿ.",

    riskManagement: "ಅಪಾಯ ನಿರ್ವಹಣೆ",
    riskManagementDesc: "ಅಪಾಯ ಮಟ್ಟಗಳನ್ನು ಗಮನಿಸಿ ಮತ್ತು ಕ್ರಮ ಕೈಗೊಳ್ಳಿ.",

    checkHealth: "ಪಶು ಆರೋಗ್ಯ ಪರಿಶೀಲಿಸಿ",
    animalType: "ಪಶುವಿನ ಪ್ರಕಾರ",
    village: "ಗ್ರಾಮದ ಹೆಸರು",
    symptoms: "ಲಕ್ಷಣಗಳು",
    daysSick: "ಅನಾರೋಗ್ಯದ ದಿನಗಳು",
    submit: "ವರದಿ ಸಲ್ಲಿಸಿ",

    selectAnimal: "ಪಶುವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    enterVillage: "ಗ್ರಾಮದ ಹೆಸರು ನಮೂದಿಸಿ",
    selectSymptoms: "ಕಾಣುವ ಎಲ್ಲಾ ಲಕ್ಷಣಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ",

    riskResult: "ಆರೋಗ್ಯ ಅಪಾಯ ಫಲಿತಾಂಶ",
    riskScore: "ಅಪಾಯ ಅಂಕ",
    riskLevel: "ಅಪಾಯ ಮಟ್ಟ",
    possibleConditions: "ಸಂಭಾವ್ಯ ಎಚ್ಚರಿಕೆ ಮಾದರಿಗಳು",
    careAdvice: "ಆರೈಕೆ ಸಲಹೆಗಳು",

    critical: "ತೀವ್ರ ಅಪಾಯ",
    high: "ಹೆಚ್ಚಿನ ಅಪಾಯ",
    moderate: "ಮಧ್ಯಮ ಅಪಾಯ",
    mild: "ಕಡಿಮೆ ಅಪಾಯ",
    noRisk: "ಗಮನಾರ್ಹ ಅಪಾಯ ಕಂಡುಬಂದಿಲ್ಲ",

    totalReports: "ಒಟ್ಟು ವರದಿಗಳು",
    highCases: "ಹೆಚ್ಚಿನ ಅಪಾಯದ ಪ್ರಕರಣಗಳು",
    lowCases: "ಕಡಿಮೆ ಅಪಾಯದ ಪ್ರಕರಣಗಳು",

    noReports: "ಯಾವುದೇ ವರದಿಗಳಿಲ್ಲ.",
    noAppointments: "ಯಾವುದೇ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳಿಲ್ಲ.",
    noNotifications: "ಯಾವುದೇ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ.",

    bookAppointment: "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಬುಕ್ ಮಾಡಿ",
    appointmentDate: "ದಿನಾಂಕ",
    appointmentTime: "ಸಮಯ",
    reason: "ಕಾರಣ",
    book: "ಬುಕ್ ಮಾಡಿ",

    pending: "ಬಾಕಿ",
    approved: "ಅನುಮೋದಿಸಲಾಗಿದೆ",
    rejected: "ತಿರಸ್ಕರಿಸಲಾಗಿದೆ",
    completed: "ಪೂರ್ಣಗೊಂಡಿದೆ",

    accept: "ಅನುಮೋದಿಸಿ",
    reject: "ತಿರಸ್ಕರಿಸಿ",
    view: "ವೀಕ್ಷಿಸಿ",

    labResult: "ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶ",
    medicine: "ಪಶುವೈದ್ಯಕೀಯ ಔಷಧಿ / ಸೂಚನೆಗಳು",
    followUp: "ಮರುಪರಿಶೀಲನೆ ಅಗತ್ಯ",
    followUpDate: "ಮರುಪರಿಶೀಲನೆ ದಿನಾಂಕ",
    notes: "ಪಶುವೈದ್ಯರ ಟಿಪ್ಪಣಿಗಳು",
    saveLab: "ವರದಿ ಉಳಿಸಿ",

    normal: "ಸಾಮಾನ್ಯ",
    needsAttention: "ಗಮನ ಅಗತ್ಯ",

    animalCareTitle: "ಪಶು ಆರೈಕೆ ಮಾರ್ಗದರ್ಶಿ",
    supportiveCare: "ಬೆಂಬಲ ಆರೈಕೆ",
    veterinaryCare: "ಪಶುವೈದ್ಯಕೀಯ ಆರೈಕೆ",

    villageRiskTitle: "ಗ್ರಾಮದ ಆರೋಗ್ಯ ಅಪಾಯ",
    animalCount: "ಪಶು ವರದಿಗಳು",
    averageRisk: "ಅಪಾಯ ಅಂಕ",

    riskManagementTitle: "ಅಪಾಯ ನಿರ್ವಹಣೆ",
    monitor: "ಮೇಲ್ವಿಚಾರಣೆ",
    action: "ಸೂಚಿಸಿದ ಕ್ರಮ",

    low: "ಕಡಿಮೆ",
    medium: "ಮಧ್ಯಮ",

    successProfile: "ಪ್ರೊಫೈಲ್ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ.",
    successReport: "ಆರೋಗ್ಯ ವರದಿ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ.",
    successAppointment: "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿ ಸಲ್ಲಿಸಲಾಗಿದೆ.",
    successLab: "ವರದಿ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ.",

    error: "ಏನೋ ತಪ್ಪಾಗಿದೆ.",
    loading: "ಲೋಡ್ ಆಗುತ್ತಿದೆ...",

    demoData: "ಡೆಮೊ ಡೇಟಾ",
    demoProfiles: "ಡೆಮೊ ಪ್ರೊಫೈಲ್‌ಗಳು",
    useDemo: "ಡೆಮೊ ಬಳಸಿ",

    farmerDemo: "ರೈತ ಡೆಮೊ",
    vetDemo: "ಪಶುವೈದ್ಯ ಡೆಮೊ",
    governmentDemo: "ಸರ್ಕಾರಿ ಡೆಮೊ",

    demoCredentials: "ಡೆಮೊ ಪ್ರೊಫೈಲ್ ವಿವರಗಳು",

    demoFarmerDetails: "ಡೆಮೊ ರೈತ • 9000000001",
    demoVetDetails: "ಡೆಮೊ ಪಶುವೈದ್ಯ • 9000000002",
    demoGovernmentDetails: "ಡೆಮೊ ಸರ್ಕಾರ • 9000000003",

    respiratoryWarning: "ಉಸಿರಾಟದ ಕಾಯಿಲೆಯ ಎಚ್ಚರಿಕೆ",
    digestiveWarning: "ಜೀರ್ಣಕ್ರಿಯೆ / ನಿರ್ಜಲೀಕರಣದ ಎಚ್ಚರಿಕೆ",
    skinWarning: "ಚರ್ಮ ಅಥವಾ ಪರೋಪಜೀವಿ ಎಚ್ಚರಿಕೆ",
    injuryWarning: "ಗಾಯ ಅಥವಾ ಉರಿಯೂತದ ಎಚ್ಚರಿಕೆ",
    generalWarning: "ಸಾಮಾನ್ಯ ಕಾಯಿಲೆ / ಪೋಷಣೆಯ ಎಚ್ಚರಿಕೆ",
    milkWarning: "ಹಾಲು ಉತ್ಪಾದನೆ / ಕೆಚ್ಚಲಿನ ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆ",
    neurologicalWarning: "ನರವ್ಯವಸ್ಥೆಯ ಎಚ್ಚರಿಕೆ",

    cleanWater: "ಶುದ್ಧ ನೀರು ನೀಡಿ ಮತ್ತು ಪಶುವನ್ನು ಆರಾಮದಾಯಕ ಸ್ಥಳದಲ್ಲಿಡಿ.",
    vetRecommended: "ಪಶುವೈದ್ಯಕೀಯ ಪರೀಕ್ಷೆ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ.",
    urgentVet: "ತಕ್ಷಣ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    noPrescription: "ಪಶುವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಔಷಧಿ ನೀಡಬೇಡಿ.",

    cow: "ಹಸು",
    buffalo: "ಎಮ್ಮೆ",
    goat: "ಮೇಕೆ",
    sheep: "ಕುರಿ",
    chicken: "ಕೋಳಿ",
    duck: "ಬಾತುಕೋಳಿ",
    pig: "ಹಂದಿ",
    dog: "ನಾಯಿ",
    cat: "ಬೆಕ್ಕು",
    horse: "ಕುದುರೆ",
    donkey: "ಕತ್ತೆ",
    camel: "ಒಂಟೆ",
    rabbit: "ಮೊಲ",
    turkey: "ಟರ್ಕಿ",
    pigeon: "ಪಾರಿವಾಳ",

    fever: "ಜ್ವರ",
    cough: "ಕೆಮ್ಮು",
    diarrhea: "ಅತಿಸಾರ",
    vomiting: "ವಾಂತಿ",
    not_eating: "ತಿನ್ನುತ್ತಿಲ್ಲ",
    reduced_eating: "ಕಡಿಮೆ ತಿನ್ನುವುದು",
    weakness: "ದೌರ್ಬಲ್ಯ",
    lethargy: "ಆಲಸ್ಯ",
    difficulty_breathing: "ಉಸಿರಾಟದ ತೊಂದರೆ",
    nasal_discharge: "ಮೂಗಿನಿಂದ ಸ್ರಾವ",
    eye_discharge: "ಕಣ್ಣಿನಿಂದ ಸ್ರಾವ",
    swelling: "ಊತ",
    skin_lesions: "ಚರ್ಮದ ಗಾಯಗಳು",
    itching: "ತುರಿಕೆ",
    hair_loss: "ಕೂದಲು ಉದುರುವುದು",
    wounds: "ಗಾಯಗಳು",
    lameness: "ಕುಂಟು",
    abdominal_swelling: "ಹೊಟ್ಟೆ ಊತ",
    bloating: "ಹೊಟ್ಟೆ ಉಬ್ಬುವುದು",
    mouth_sores: "ಬಾಯಿಯ ಗಾಯಗಳು",
    excessive_salivation: "ಹೆಚ್ಚಿನ ಲಾಲಾರಸ",
    milk_drop: "ಹಾಲು ಕಡಿಮೆಯಾಗುವುದು",
    abnormal_milk: "ಅಸಹಜ ಹಾಲು",
    weight_loss: "ತೂಕ ಇಳಿಕೆ",
    constipation: "ಮಲಬದ್ಧತೆ",
    tremors: "ನಡುಕ",
    seizures: "ಸೆಳೆತ",
    bleeding: "ರಕ್ತಸ್ರಾವ",
    high_thirst: "ಹೆಚ್ಚಿನ ದಾಹ",
    frequent_urination: "ಹೆಚ್ಚು ಮೂತ್ರ ವಿಸರ್ಜನೆ",
    reproductive_problem: "ಸಂತಾನೋತ್ಪತ್ತಿ ಸಮಸ್ಯೆ",
    ticks: "ಉಣ್ಣಿ",
    dehydration: "ನಿರ್ಜಲೀಕರಣ",
    discharge: "ಅಸಹಜ ಸ್ರಾವ"
  },


  Hindi: {

    appName: "पशुरक्षा",
    tagline: "स्मार्ट पशु स्वास्थ्य और पशु चिकित्सा सहायता",

    profile: "प्रोफ़ाइल",
    fullName: "पूरा नाम",
    mobile: "मोबाइल नंबर",
    role: "भूमिका",
    language: "भाषा",
    save: "सहेजें और आगे बढ़ें",

    farmer: "किसान",
    veterinary: "पशु चिकित्सक",
    government: "सरकार",

    farmerPortal: "किसान पोर्टल",
    veterinaryPortal: "पशु चिकित्सा पोर्टल",
    governmentPortal: "सरकारी पोर्टल",

    welcome: "स्वागत है",
    backProfile: "प्रोफ़ाइल पर वापस जाएँ",
    readAloud: "🔊 पढ़कर सुनाएँ",

    animalHealth: "पशु स्वास्थ्य जाँच",
    animalHealthDesc: "लक्षणों के आधार पर पशु स्वास्थ्य जोखिम जाँचें.",

    appointments: "अपॉइंटमेंट",
    appointmentsDesc: "पशु चिकित्सक से अपॉइंटमेंट बुक करें.",

    reports: "मेरी रिपोर्ट",
    reportsDesc: "आपके द्वारा भेजी गई स्वास्थ्य रिपोर्ट देखें.",

    notifications: "सूचनाएँ",
    notificationsDesc: "स्वास्थ्य और अपॉइंटमेंट अपडेट देखें.",

    animalCare: "पशु देखभाल",
    animalCareDesc: "सामान्य पशु स्वास्थ्य समस्याएँ और देखभाल जानें.",

    animalReports: "पशु रिपोर्ट",
    animalReportsDesc: "किसानों द्वारा भेजी गई रिपोर्ट देखें.",

    appointmentRequests: "अपॉइंटमेंट अनुरोध",
    appointmentRequestsDesc: "किसानों के पशु चिकित्सा अनुरोधों की समीक्षा करें.",

    laboratory: "प्रयोगशाला",
    laboratoryDesc: "पशु चिकित्सा जाँच और प्रयोगशाला परिणाम जोड़ें.",

    villageRisk: "गाँव का जोखिम",
    villageRiskDesc: "गाँवों में पशु स्वास्थ्य जोखिम देखें.",

    riskManagement: "जोखिम प्रबंधन",
    riskManagementDesc: "जोखिम स्तर देखें और कार्रवाई की योजना बनाएँ.",

    checkHealth: "पशु स्वास्थ्य जाँचें",
    animalType: "पशु का प्रकार",
    village: "गाँव का नाम",
    symptoms: "लक्षण",
    daysSick: "बीमारी के दिन",
    submit: "रिपोर्ट भेजें",

    selectAnimal: "पशु चुनें",
    enterVillage: "गाँव का नाम लिखें",
    selectSymptoms: "दिखाई देने वाले सभी लक्षण चुनें",

    riskResult: "स्वास्थ्य जोखिम परिणाम",
    riskScore: "जोखिम स्कोर",
    riskLevel: "जोखिम स्तर",
    possibleConditions: "संभावित चेतावनी",
    careAdvice: "देखभाल सलाह",

    critical: "गंभीर",
    high: "उच्च जोखिम",
    moderate: "मध्यम जोखिम",
    mild: "हल्का जोखिम",
    noRisk: "कोई महत्वपूर्ण जोखिम नहीं",

    totalReports: "कुल रिपोर्ट",
    highCases: "उच्च जोखिम मामले",
    lowCases: "कम जोखिम मामले",

    noReports: "कोई रिपोर्ट नहीं.",
    noAppointments: "कोई अपॉइंटमेंट नहीं.",
    noNotifications: "कोई सूचना नहीं.",

    bookAppointment: "अपॉइंटमेंट बुक करें",
    appointmentDate: "तारीख",
    appointmentTime: "समय",
    reason: "कारण",
    book: "बुक करें",

    pending: "लंबित",
    approved: "स्वीकृत",
    rejected: "अस्वीकृत",
    completed: "पूर्ण",

    accept: "स्वीकृत करें",
    reject: "अस्वीकार करें",
    view: "देखें",

    labResult: "प्रयोगशाला / जाँच परिणाम",
    medicine: "पशु चिकित्सा दवा / निर्देश",
    followUp: "फॉलो-अप आवश्यक",
    followUpDate: "फॉलो-अप तारीख",
    notes: "पशु चिकित्सक की टिप्पणी",
    saveLab: "रिपोर्ट सहेजें",

    normal: "सामान्य",
    needsAttention: "ध्यान आवश्यक",

    animalCareTitle: "पशु देखभाल मार्गदर्शिका",
    supportiveCare: "सहायक देखभाल",
    veterinaryCare: "पशु चिकित्सा देखभाल",

    villageRiskTitle: "गाँव स्वास्थ्य जोखिम",
    animalCount: "पशु रिपोर्ट",
    averageRisk: "जोखिम स्कोर",

    riskManagementTitle: "जोखिम प्रबंधन",
    monitor: "निगरानी",
    action: "सुझाई गई कार्रवाई",

    low: "कम",
    medium: "मध्यम",

    successProfile: "प्रोफ़ाइल सफलतापूर्वक सहेजी गई.",
    successReport: "स्वास्थ्य रिपोर्ट सफलतापूर्वक भेजी गई.",
    successAppointment: "अपॉइंटमेंट अनुरोध भेजा गया.",
    successLab: "रिपोर्ट सफलतापूर्वक सहेजी गई.",

    error: "कुछ गलत हुआ.",
    loading: "लोड हो रहा है...",

    demoData: "डेमो डेटा",
    demoProfiles: "डेमो प्रोफ़ाइल",
    useDemo: "डेमो इस्तेमाल करें",

    farmerDemo: "किसान डेमो",
    vetDemo: "पशु चिकित्सक डेमो",
    governmentDemo: "सरकारी डेमो",

    demoCredentials: "डेमो प्रोफ़ाइल विवरण",

    demoFarmerDetails: "डेमो किसान • 9000000001",
    demoVetDetails: "डेमो पशु चिकित्सक • 9000000002",
    demoGovernmentDetails: "डेमो सरकार • 9000000003",

    respiratoryWarning: "श्वसन बीमारी की चेतावनी",
    digestiveWarning: "पाचन / निर्जलीकरण की चेतावनी",
    skinWarning: "त्वचा या परजीवी चेतावनी",
    injuryWarning: "चोट या सूजन की चेतावनी",
    generalWarning: "सामान्य बीमारी / पोषण चेतावनी",
    milkWarning: "दूध उत्पादन / थन स्वास्थ्य चेतावनी",
    neurologicalWarning: "तंत्रिका संबंधी चेतावनी",

    cleanWater: "साफ पानी दें और पशु को आरामदायक जगह पर रखें.",
    vetRecommended: "पशु चिकित्सक की जाँच की सलाह दी जाती है.",
    urgentVet: "जल्द पशु चिकित्सक से संपर्क करें.",
    noPrescription: "पशु चिकित्सक की सलाह के बिना दवा न दें.",

    cow: "गाय",
    buffalo: "भैंस",
    goat: "बकरी",
    sheep: "भेड़",
    chicken: "मुर्गी",
    duck: "बत्तख",
    pig: "सूअर",
    dog: "कुत्ता",
    cat: "बिल्ली",
    horse: "घोड़ा",
    donkey: "गधा",
    camel: "ऊँट",
    rabbit: "खरगोश",
    turkey: "टर्की",
    pigeon: "कबूतर",

    fever: "बुखार",
    cough: "खाँसी",
    diarrhea: "दस्त",
    vomiting: "उल्टी",
    not_eating: "खाना नहीं खाना",
    reduced_eating: "कम खाना",
    weakness: "कमज़ोरी",
    lethargy: "सुस्ती",
    difficulty_breathing: "साँस लेने में कठिनाई",
    nasal_discharge: "नाक से स्राव",
    eye_discharge: "आँख से स्राव",
    swelling: "सूजन",
    skin_lesions: "त्वचा के घाव",
    itching: "खुजली",
    hair_loss: "बाल झड़ना",
    wounds: "घाव",
    lameness: "लंगड़ाना",
    abdominal_swelling: "पेट में सूजन",
    bloating: "पेट फूलना",
    mouth_sores: "मुँह में घाव",
    excessive_salivation: "अधिक लार",
    milk_drop: "दूध कम होना",
    abnormal_milk: "असामान्य दूध",
    weight_loss: "वजन कम होना",
    constipation: "कब्ज",
    tremors: "कंपकंपी",
    seizures: "दौरे",
    bleeding: "खून आना",
    high_thirst: "अधिक प्यास",
    frequent_urination: "बार-बार पेशाब",
    reproductive_problem: "प्रजनन समस्या",
    ticks: "किलनी",
    dehydration: "निर्जलीकरण",
    discharge: "असामान्य स्राव"
  },


  Telugu: {

    appName: "పశురక్ష",
    tagline: "స్మార్ట్ పశు ఆరోగ్యం మరియు పశువైద్య సహాయం",

    profile: "ప్రొఫైల్",
    fullName: "పూర్తి పేరు",
    mobile: "మొబైల్ నంబర్",
    role: "పాత్ర",
    language: "భాష",
    save: "సేవ్ చేసి కొనసాగించండి",

    farmer: "రైతు",
    veterinary: "పశువైద్యుడు",
    government: "ప్రభుత్వం",

    farmerPortal: "రైతు పోర్టల్",
    veterinaryPortal: "పశువైద్య పోర్టల్",
    governmentPortal: "ప్రభుత్వ పోర్టల్",

    welcome: "స్వాగతం",
    backProfile: "ప్రొఫైల్‌కు తిరిగి వెళ్లండి",
    readAloud: "🔊 చదివి వినిపించండి",

    animalHealth: "పశు ఆరోగ్య పరీక్ష",
    animalHealthDesc: "లక్షణాల ఆధారంగా పశు ఆరోగ్య ప్రమాదాన్ని పరిశీలించండి.",

    appointments: "అపాయింట్‌మెంట్లు",
    appointmentsDesc: "పశువైద్య అపాయింట్‌మెంట్ బుక్ చేయండి.",

    reports: "నా నివేదికలు",
    reportsDesc: "మీరు సమర్పించిన ఆరోగ్య నివేదికలను చూడండి.",

    notifications: "నోటిఫికేషన్లు",
    notificationsDesc: "ఆరోగ్యం మరియు అపాయింట్‌మెంట్ నవీకరణలను చూడండి.",

    animalCare: "పశు సంరక్షణ",
    animalCareDesc: "సాధారణ పశు ఆరోగ్య సమస్యలు మరియు సంరక్షణ తెలుసుకోండి.",

    animalReports: "పశు నివేదికలు",
    animalReportsDesc: "రైతులు సమర్పించిన పశు ఆరోగ్య నివేదికలను చూడండి.",

    appointmentRequests: "అపాయింట్‌మెంట్ అభ్యర్థనలు",
    appointmentRequestsDesc: "రైతుల పశువైద్య అభ్యర్థనలను సమీక్షించండి.",

    laboratory: "ప్రయోగశాల",
    laboratoryDesc: "పశువైద్య పరీక్ష మరియు ప్రయోగశాల ఫలితాలను జోడించండి.",

    villageRisk: "గ్రామ ప్రమాదం",
    villageRiskDesc: "గ్రామాల పశు ఆరోగ్య ప్రమాదాన్ని పర్యవేక్షించండి.",

    riskManagement: "ప్రమాద నిర్వహణ",
    riskManagementDesc: "ప్రమాద స్థాయిలను పర్యవేక్షించి చర్యలు తీసుకోండి.",

    checkHealth: "పశు ఆరోగ్యాన్ని పరీక్షించండి",
    animalType: "పశువు రకం",
    village: "గ్రామం పేరు",
    symptoms: "లక్షణాలు",
    daysSick: "అనారోగ్య రోజులు",
    submit: "నివేదిక సమర్పించండి",

    selectAnimal: "పశువును ఎంచుకోండి",
    enterVillage: "గ్రామం పేరు నమోదు చేయండి",
    selectSymptoms: "కనిపించే అన్ని లక్షణాలను ఎంచుకోండి",

    riskResult: "ఆరోగ్య ప్రమాద ఫలితం",
    riskScore: "ప్రమాద స్కోర్",
    riskLevel: "ప్రమాద స్థాయి",
    possibleConditions: "సంభావ్య హెచ్చరికలు",
    careAdvice: "సంరక్షణ సూచనలు",

    critical: "తీవ్రమైన",
    high: "అధిక ప్రమాదం",
    moderate: "మధ్యస్థ ప్రమాదం",
    mild: "తక్కువ ప్రమాదం",
    noRisk: "గణనీయమైన ప్రమాదం లేదు",

    totalReports: "మొత్తం నివేదికలు",
    highCases: "అధిక ప్రమాద కేసులు",
    lowCases: "తక్కువ ప్రమాద కేసులు",

    noReports: "నివేదికలు లేవు.",
    noAppointments: "అపాయింట్‌మెంట్లు లేవు.",
    noNotifications: "నోటిఫికేషన్లు లేవు.",

    bookAppointment: "అపాయింట్‌మెంట్ బుక్ చేయండి",
    appointmentDate: "తేదీ",
    appointmentTime: "సమయం",
    reason: "కారణం",
    book: "బుక్ చేయండి",

    pending: "పెండింగ్",
    approved: "ఆమోదించబడింది",
    rejected: "తిరస్కరించబడింది",
    completed: "పూర్తయింది",

    accept: "ఆమోదించండి",
    reject: "తిరస్కరించండి",
    view: "చూడండి",

    labResult: "ప్రయోగశాల / పరీక్ష ఫలితం",
    medicine: "పశువైద్య మందు / సూచనలు",
    followUp: "ఫాలో-అప్ అవసరం",
    followUpDate: "ఫాలో-అప్ తేదీ",
    notes: "పశువైద్య గమనికలు",
    saveLab: "నివేదిక సేవ్ చేయండి",

    normal: "సాధారణం",
    needsAttention: "శ్రద్ధ అవసరం",

    animalCareTitle: "పశు సంరక్షణ మార్గదర్శకం",
    supportiveCare: "సహాయక సంరక్షణ",
    veterinaryCare: "పశువైద్య సంరక్షణ",

    villageRiskTitle: "గ్రామ ఆరోగ్య ప్రమాదం",
    animalCount: "పశు నివేదికలు",
    averageRisk: "ప్రమాద స్కోర్",

    riskManagementTitle: "ప్రమాద నిర్వహణ",
    monitor: "పర్యవేక్షణ",
    action: "సూచించిన చర్య",

    low: "తక్కువ",
    medium: "మధ్యస్థ",

    successProfile: "ప్రొఫైల్ విజయవంతంగా సేవ్ చేయబడింది.",
    successReport: "ఆరోగ్య నివేదిక విజయవంతంగా సమర్పించబడింది.",
    successAppointment: "అపాయింట్‌మెంట్ అభ్యర్థన సమర్పించబడింది.",
    successLab: "నివేదిక విజయవంతంగా సేవ్ చేయబడింది.",

    error: "ఏదో తప్పు జరిగింది.",
    loading: "లోడ్ అవుతోంది...",

    demoData: "డెమో డేటా",
    demoProfiles: "డెమో ప్రొఫైల్స్",
    useDemo: "డెమో ఉపయోగించండి",

    farmerDemo: "రైతు డెమో",
    vetDemo: "పశువైద్య డెమో",
    governmentDemo: "ప్రభుత్వ డెమో",

    demoCredentials: "డెమో ప్రొఫైల్ వివరాలు",

    demoFarmerDetails: "డెమో రైతు • 9000000001",
    demoVetDetails: "డెమో పశువైద్యుడు • 9000000002",
    demoGovernmentDetails: "డెమో ప్రభుత్వం • 9000000003",

    respiratoryWarning: "శ్వాసకోశ వ్యాధి హెచ్చరిక",
    digestiveWarning: "జీర్ణక్రియ / డీహైడ్రేషన్ హెచ్చరిక",
    skinWarning: "చర్మం లేదా పరాన్నజీవుల హెచ్చరిక",
    injuryWarning: "గాయం లేదా వాపు హెచ్చరిక",
    generalWarning: "సాధారణ అనారోగ్యం / పోషణ హెచ్చరిక",
    milkWarning: "పాల ఉత్పత్తి / పొదుగు ఆరోగ్య హెచ్చరిక",
    neurologicalWarning: "నరాల సంబంధిత హెచ్చరిక",

    cleanWater: "శుభ్రమైన నీరు ఇవ్వండి మరియు పశువును సౌకర్యవంతమైన ప్రదేశంలో ఉంచండి.",
    vetRecommended: "పశువైద్య పరీక్ష సిఫార్సు చేయబడింది.",
    urgentVet: "వెంటనే పశువైద్యుడిని సంప్రదించండి.",
    noPrescription: "పశువైద్యుడి సలహా లేకుండా మందులు ఇవ్వవద్దు.",

    cow: "ఆవు",
    buffalo: "గేదె",
    goat: "మేక",
    sheep: "గొర్రె",
    chicken: "కోడి",
    duck: "బాతు",
    pig: "పంది",
    dog: "కుక్క",
    cat: "పిల్లి",
    horse: "గుర్రం",
    donkey: "గాడిద",
    camel: "ఒంటె",
    rabbit: "కుందేలు",
    turkey: "టర్కీ",
    pigeon: "పావురం",

    fever: "జ్వరం",
    cough: "దగ్గు",
    diarrhea: "విరేచనాలు",
    vomiting: "వాంతులు",
    not_eating: "తినకపోవడం",
    reduced_eating: "తక్కువగా తినడం",
    weakness: "బలహీనత",
    lethargy: "నీరసం",
    difficulty_breathing: "శ్వాస తీసుకోవడంలో ఇబ్బంది",
    nasal_discharge: "ముక్కు స్రావం",
    eye_discharge: "కంటి స్రావం",
    swelling: "వాపు",
    skin_lesions: "చర్మ గాయాలు",
    itching: "దురద",
    hair_loss: "జుట్టు రాలడం",
    wounds: "గాయాలు",
    lameness: "కుంటడం",
    abdominal_swelling: "కడుపు వాపు",
    bloating: "కడుపు ఉబ్బరం",
    mouth_sores: "నోటి గాయాలు",
    excessive_salivation: "అధిక లాలాజలం",
    milk_drop: "పాలు తగ్గడం",
    abnormal_milk: "అసాధారణ పాలు",
    weight_loss: "బరువు తగ్గడం",
    constipation: "మలబద్ధకం",
    tremors: "వణుకు",
    seizures: "మూర్ఛలు",
    bleeding: "రక్తస్రావం",
    high_thirst: "అధిక దాహం",
    frequent_urination: "తరచుగా మూత్రం",
    reproductive_problem: "పునరుత్పత్తి సమస్య",
    ticks: "పురుగులు",
    dehydration: "డీహైడ్రేషన్",
    discharge: "అసాధారణ స్రావం"
  },


  Tamil: {

    appName: "பசுரக்ஷா",
    tagline: "ஸ்மார்ட் கால்நடை ஆரோக்கியம் மற்றும் கால்நடை மருத்துவ உதவி",

    profile: "சுயவிவரம்",
    fullName: "முழு பெயர்",
    mobile: "மொபைல் எண்",
    role: "பங்கு",
    language: "மொழி",
    save: "சேமித்து தொடரவும்",

    farmer: "விவசாயி",
    veterinary: "கால்நடை மருத்துவர்",
    government: "அரசு",

    farmerPortal: "விவசாயி போர்டல்",
    veterinaryPortal: "கால்நடை மருத்துவ போர்டல்",
    governmentPortal: "அரசு போர்டல்",

    welcome: "வரவேற்கிறோம்",
    backProfile: "சுயவிவரத்திற்குத் திரும்பு",
    readAloud: "🔊 வாசித்து கேட்க",

    animalHealth: "கால்நடை ஆரோக்கிய பரிசோதனை",
    animalHealthDesc: "அறிகுறிகளின் அடிப்படையில் கால்நடை ஆரோக்கிய அபாயத்தை பார்க்கவும்.",

    appointments: "சந்திப்புகள்",
    appointmentsDesc: "கால்நடை மருத்துவரை சந்திக்க நேரம் பதிவு செய்யவும்.",

    reports: "என் அறிக்கைகள்",
    reportsDesc: "நீங்கள் சமர்ப்பித்த ஆரோக்கிய அறிக்கைகளைப் பார்க்கவும்.",

    notifications: "அறிவிப்புகள்",
    notificationsDesc: "ஆரோக்கியம் மற்றும் சந்திப்பு புதுப்பிப்புகளைப் பார்க்கவும்.",

    animalCare: "கால்நடை பராமரிப்பு",
    animalCareDesc: "பொதுவான கால்நடை பிரச்சினைகள் மற்றும் பராமரிப்பை அறியவும்.",

    animalReports: "கால்நடை அறிக்கைகள்",
    animalReportsDesc: "விவசாயிகள் சமர்ப்பித்த அறிக்கைகளைப் பார்க்கவும்.",

    appointmentRequests: "சந்திப்பு கோரிக்கைகள்",
    appointmentRequestsDesc: "விவசாயிகளின் கால்நடை மருத்துவ கோரிக்கைகளைப் பார்க்கவும்.",

    laboratory: "ஆய்வகம்",
    laboratoryDesc: "கால்நடை பரிசோதனை மற்றும் ஆய்வக முடிவுகளைச் சேர்க்கவும்.",

    villageRisk: "கிராம அபாயம்",
    villageRiskDesc: "கிராமங்களின் கால்நடை ஆரோக்கிய அபாயத்தை கண்காணிக்கவும்.",

    riskManagement: "அபாய மேலாண்மை",
    riskManagementDesc: "அபாய நிலைகளை கண்காணித்து நடவடிக்கை எடுக்கவும்.",

    checkHealth: "கால்நடை ஆரோக்கியத்தைச் சரிபார்க்கவும்",
    animalType: "கால்நடை வகை",
    village: "கிராமத்தின் பெயர்",
    symptoms: "அறிகுறிகள்",
    daysSick: "நோய்வாய்ப்பட்ட நாட்கள்",
    submit: "அறிக்கையை சமர்ப்பிக்கவும்",

    selectAnimal: "கால்நடையைத் தேர்ந்தெடுக்கவும்",
    enterVillage: "கிராமத்தின் பெயரை உள்ளிடவும்",
    selectSymptoms: "காணப்படும் அனைத்து அறிகுறிகளையும் தேர்ந்தெடுக்கவும்",

    riskResult: "ஆரோக்கிய அபாய முடிவு",
    riskScore: "அபாய மதிப்பெண்",
    riskLevel: "அபாய நிலை",
    possibleConditions: "சாத்தியமான எச்சரிக்கைகள்",
    careAdvice: "பராமரிப்பு ஆலோசனை",

    critical: "மிகவும் தீவிரம்",
    high: "அதிக அபாயம்",
    moderate: "மிதமான அபாயம்",
    mild: "குறைந்த அபாயம்",
    noRisk: "குறிப்பிடத்தக்க அபாயம் இல்லை",

    totalReports: "மொத்த அறிக்கைகள்",
    highCases: "அதிக அபாய வழக்குகள்",
    lowCases: "குறைந்த அபாய வழக்குகள்",

    noReports: "அறிக்கைகள் இல்லை.",
    noAppointments: "சந்திப்புகள் இல்லை.",
    noNotifications: "அறிவிப்புகள் இல்லை.",

    bookAppointment: "சந்திப்பு பதிவு செய்யவும்",
    appointmentDate: "தேதி",
    appointmentTime: "நேரம்",
    reason: "காரணம்",
    book: "பதிவு செய்யவும்",

    pending: "நிலுவையில்",
    approved: "அங்கீகரிக்கப்பட்டது",
    rejected: "நிராகரிக்கப்பட்டது",
    completed: "முடிந்தது",

    accept: "அங்கீகரிக்கவும்",
    reject: "நிராகரிக்கவும்",
    view: "பார்க்கவும்",

    labResult: "ஆய்வக / பரிசோதனை முடிவு",
    medicine: "கால்நடை மருந்து / வழிமுறைகள்",
    followUp: "மீண்டும் பரிசோதனை தேவை",
    followUpDate: "மீண்டும் பரிசோதனை தேதி",
    notes: "மருத்துவர் குறிப்புகள்",
    saveLab: "அறிக்கையை சேமிக்கவும்",

    normal: "இயல்பானது",
    needsAttention: "கவனம் தேவை",

    animalCareTitle: "கால்நடை பராமரிப்பு வழிகாட்டி",
    supportiveCare: "ஆதரவு பராமரிப்பு",
    veterinaryCare: "கால்நடை மருத்துவ பராமரிப்பு",

    villageRiskTitle: "கிராம ஆரோக்கிய அபாயம்",
    animalCount: "கால்நடை அறிக்கைகள்",
    averageRisk: "அபாய மதிப்பெண்",

    riskManagementTitle: "அபாய மேலாண்மை",
    monitor: "கண்காணிப்பு",
    action: "பரிந்துரைக்கப்பட்ட நடவடிக்கை",

    low: "குறைவு",
    medium: "மிதமான",

    successProfile: "சுயவிவரம் வெற்றிகரமாக சேமிக்கப்பட்டது.",
    successReport: "ஆரோக்கிய அறிக்கை வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது.",
    successAppointment: "சந்திப்பு கோரிக்கை சமர்ப்பிக்கப்பட்டது.",
    successLab: "அறிக்கை வெற்றிகரமாக சேமிக்கப்பட்டது.",

    error: "ஏதோ தவறு ஏற்பட்டது.",
    loading: "ஏற்றுகிறது...",

    demoData: "டெமோ தரவு",
    demoProfiles: "டெமோ சுயவிவரங்கள்",
    useDemo: "டெமோ பயன்படுத்தவும்",

    farmerDemo: "விவசாயி டெமோ",
    vetDemo: "மருத்துவர் டெமோ",
    governmentDemo: "அரசு டெமோ",

    demoCredentials: "டெமோ சுயவிவர விவரங்கள்",

    demoFarmerDetails: "டெமோ விவசாயி • 9000000001",
    demoVetDetails: "டெமோ மருத்துவர் • 9000000002",
    demoGovernmentDetails: "டெமோ அரசு • 9000000003",

    respiratoryWarning: "சுவாச நோய் எச்சரிக்கை",
    digestiveWarning: "செரிமானம் / நீரிழப்பு எச்சரிக்கை",
    skinWarning: "தோல் அல்லது ஒட்டுண்ணி எச்சரிக்கை",
    injuryWarning: "காயம் அல்லது வீக்கம் எச்சரிக்கை",
    generalWarning: "பொதுவான நோய் / ஊட்டச்சத்து எச்சரிக்கை",
    milkWarning: "பால் உற்பத்தி / மடி ஆரோக்கிய எச்சரிக்கை",
    neurologicalWarning: "நரம்பியல் எச்சரிக்கை",

    cleanWater: "சுத்தமான குடிநீர் வழங்கி, கால்நடையை வசதியான இடத்தில் வைக்கவும்.",
    vetRecommended: "கால்நடை மருத்துவர் பரிசோதனை பரிந்துரைக்கப்படுகிறது.",
    urgentVet: "உடனடியாக கால்நடை மருத்துவரை அணுகவும்.",
    noPrescription: "மருத்துவர் ஆலோசனை இல்லாமல் மருந்து கொடுக்க வேண்டாம்.",

    cow: "பசு",
    buffalo: "எருமை",
    goat: "ஆடு",
    sheep: "செம்மறியாடு",
    chicken: "கோழி",
    duck: "வாத்து",
    pig: "பன்றி",
    dog: "நாய்",
    cat: "பூனை",
    horse: "குதிரை",
    donkey: "கழுதை",
    camel: "ஒட்டகம்",
    rabbit: "முயல்",
    turkey: "வான்கோழி",
    pigeon: "புறா",

    fever: "காய்ச்சல்",
    cough: "இருமல்",
    diarrhea: "வயிற்றுப்போக்கு",
    vomiting: "வாந்தி",
    not_eating: "சாப்பிடாமல் இருப்பது",
    reduced_eating: "குறைவாக சாப்பிடுதல்",
    weakness: "பலவீனம்",
    lethargy: "சோர்வு",
    difficulty_breathing: "சுவாசிப்பதில் சிரமம்",
    nasal_discharge: "மூக்கில் சுரப்பு",
    eye_discharge: "கண்ணில் சுரப்பு",
    swelling: "வீக்கம்",
    skin_lesions: "தோல் புண்கள்",
    itching: "அரிப்பு",
    hair_loss: "முடி உதிர்தல்",
    wounds: "காயங்கள்",
    lameness: "நொண்டுதல்",
    abdominal_swelling: "வயிற்று வீக்கம்",
    bloating: "வயிறு உப்புசம்",
    mouth_sores: "வாய் புண்கள்",
    excessive_salivation: "அதிக உமிழ்நீர்",
    milk_drop: "பால் உற்பத்தி குறைவு",
    abnormal_milk: "அசாதாரண பால்",
    weight_loss: "எடை குறைதல்",
    constipation: "மலச்சிக்கல்",
    tremors: "நடுக்கம்",
    seizures: "வலிப்பு",
    bleeding: "இரத்தப்போக்கு",
    high_thirst: "அதிக தாகம்",
    frequent_urination: "அடிக்கடி சிறுநீர்",
    reproductive_problem: "இனப்பெருக்க பிரச்சினை",
    ticks: "உண்ணிகள்",
    dehydration: "நீரிழப்பு",
    discharge: "அசாதாரண சுரப்பு"
  },


  Marathi: {

    appName: "पशुरक्षा",
    tagline: "स्मार्ट पशुधन आरोग्य आणि पशुवैद्यकीय सहाय्य",

    profile: "प्रोफाइल",
    fullName: "पूर्ण नाव",
    mobile: "मोबाईल क्रमांक",
    role: "भूमिका",
    language: "भाषा",
    save: "जतन करा आणि पुढे जा",

    farmer: "शेतकरी",
    veterinary: "पशुवैद्य",
    government: "सरकार",

    farmerPortal: "शेतकरी पोर्टल",
    veterinaryPortal: "पशुवैद्यकीय पोर्टल",
    governmentPortal: "सरकारी पोर्टल",

    welcome: "स्वागत",
    backProfile: "प्रोफाइलवर परत जा",
    readAloud: "🔊 मोठ्याने वाचा",

    animalHealth: "पशु आरोग्य तपासणी",
    animalHealthDesc: "लक्षणांवर आधारित पशु आरोग्याचा धोका तपासा.",

    appointments: "भेटी",
    appointmentsDesc: "पशुवैद्यकीय भेट बुक करा.",

    reports: "माझे अहवाल",
    reportsDesc: "तुम्ही पाठवलेले आरोग्य अहवाल पहा.",

    notifications: "सूचना",
    notificationsDesc: "आरोग्य आणि भेटींचे अपडेट पहा.",

    animalCare: "पशु काळजी",
    animalCareDesc: "सामान्य पशु आरोग्य समस्या आणि काळजी जाणून घ्या.",

    animalReports: "पशु अहवाल",
    animalReportsDesc: "शेतकऱ्यांनी पाठवलेले अहवाल पहा.",

    appointmentRequests: "भेटीच्या विनंत्या",
    appointmentRequestsDesc: "शेतकऱ्यांच्या पशुवैद्यकीय विनंत्या पहा.",

    laboratory: "प्रयोगशाळा",
    laboratoryDesc: "पशुवैद्यकीय तपासणी आणि प्रयोगशाळेचे निकाल जोडा.",

    villageRisk: "गावाचा धोका",
    villageRiskDesc: "गावांमधील पशु आरोग्य धोका पहा.",

    riskManagement: "धोका व्यवस्थापन",
    riskManagementDesc: "धोका पातळी पाहून उपाययोजना करा.",

    checkHealth: "पशु आरोग्य तपासा",
    animalType: "पशु प्रकार",
    village: "गावाचे नाव",
    symptoms: "लक्षणे",
    daysSick: "आजारी दिवस",
    submit: "अहवाल पाठवा",

    selectAnimal: "पशु निवडा",
    enterVillage: "गावाचे नाव लिहा",
    selectSymptoms: "दिसणारी सर्व लक्षणे निवडा",

    riskResult: "आरोग्य धोका निकाल",
    riskScore: "धोका गुण",
    riskLevel: "धोका पातळी",
    possibleConditions: "संभाव्य इशारे",
    careAdvice: "काळजीचा सल्ला",

    critical: "गंभीर",
    high: "उच्च धोका",
    moderate: "मध्यम धोका",
    mild: "कमी धोका",
    noRisk: "महत्त्वाचा धोका आढळला नाही",

    totalReports: "एकूण अहवाल",
    highCases: "उच्च धोका प्रकरणे",
    lowCases: "कमी धोका प्रकरणे",

    noReports: "अहवाल उपलब्ध नाहीत.",
    noAppointments: "भेटी उपलब्ध नाहीत.",
    noNotifications: "सूचना उपलब्ध नाहीत.",

    bookAppointment: "भेट बुक करा",
    appointmentDate: "तारीख",
    appointmentTime: "वेळ",
    reason: "कारण",
    book: "बुक करा",

    pending: "प्रलंबित",
    approved: "मंजूर",
    rejected: "नाकारले",
    completed: "पूर्ण",

    accept: "मंजूर करा",
    reject: "नकार द्या",
    view: "पहा",

    labResult: "प्रयोगशाळा / तपासणी निकाल",
    medicine: "पशुवैद्यकीय औषध / सूचना",
    followUp: "फॉलो-अप आवश्यक",
    followUpDate: "फॉलो-अप तारीख",
    notes: "पशुवैद्यकीय नोंदी",
    saveLab: "अहवाल जतन करा",

    normal: "सामान्य",
    needsAttention: "लक्ष आवश्यक",

    animalCareTitle: "पशु काळजी मार्गदर्शक",
    supportiveCare: "सहाय्यक काळजी",
    veterinaryCare: "पशुवैद्यकीय काळजी",

    villageRiskTitle: "गाव आरोग्य धोका",
    animalCount: "पशु अहवाल",
    averageRisk: "धोका गुण",

    riskManagementTitle: "धोका व्यवस्थापन",
    monitor: "निरीक्षण",
    action: "सुचवलेली कृती",

    low: "कमी",
    medium: "मध्यम",

    successProfile: "प्रोफाइल यशस्वीरित्या जतन झाले.",
    successReport: "आरोग्य अहवाल यशस्वीरित्या पाठवला.",
    successAppointment: "भेटीची विनंती पाठवली.",
    successLab: "अहवाल यशस्वीरित्या जतन झाला.",

    error: "काहीतरी चूक झाली.",
    loading: "लोड होत आहे...",

    demoData: "डेमो डेटा",
    demoProfiles: "डेमो प्रोफाइल",
    useDemo: "डेमो वापरा",

    farmerDemo: "शेतकरी डेमो",
    vetDemo: "पशुवैद्य डेमो",
    governmentDemo: "सरकारी डेमो",

    demoCredentials: "डेमो प्रोफाइल तपशील",

    demoFarmerDetails: "डेमो शेतकरी • 9000000001",
    demoVetDetails: "डेमो पशुवैद्य • 9000000002",
    demoGovernmentDetails: "डेमो सरकार • 9000000003",

    respiratoryWarning: "श्वसन आजाराचा इशारा",
    digestiveWarning: "पचन / निर्जलीकरणाचा इशारा",
    skinWarning: "त्वचा किंवा परजीवी इशारा",
    injuryWarning: "इजा किंवा सूज इशारा",
    generalWarning: "सामान्य आजार / पोषण इशारा",
    milkWarning: "दूध उत्पादन / कास आरोग्य इशारा",
    neurologicalWarning: "न्यूरोलॉजिकल इशारा",

    cleanWater: "स्वच्छ पाणी द्या आणि पशूला आरामदायी ठिकाणी ठेवा.",
    vetRecommended: "पशुवैद्यकीय तपासणीची शिफारस केली जाते.",
    urgentVet: "लवकरात लवकर पशुवैद्याशी संपर्क करा.",
    noPrescription: "पशुवैद्यकीय सल्ल्याशिवाय औषध देऊ नका.",

    cow: "गाय",
    buffalo: "म्हैस",
    goat: "शेळी",
    sheep: "मेंढी",
    chicken: "कोंबडी",
    duck: "बदक",
    pig: "डुक्कर",
    dog: "कुत्रा",
    cat: "मांजर",
    horse: "घोडा",
    donkey: "गाढव",
    camel: "उंट",
    rabbit: "ससा",
    turkey: "टर्की",
    pigeon: "कबूतर",

    fever: "ताप",
    cough: "खोकला",
    diarrhea: "अतिसार",
    vomiting: "उलटी",
    not_eating: "खात नाही",
    reduced_eating: "कमी खाणे",
    weakness: "अशक्तपणा",
    lethargy: "सुस्ती",
    difficulty_breathing: "श्वास घेण्यास त्रास",
    nasal_discharge: "नाकातून स्राव",
    eye_discharge: "डोळ्यातून स्राव",
    swelling: "सूज",
    skin_lesions: "त्वचेवरील जखमा",
    itching: "खाज",
    hair_loss: "केस गळणे",
    wounds: "जखमा",
    lameness: "लंगडणे",
    abdominal_swelling: "पोटाची सूज",
    bloating: "पोट फुगणे",
    mouth_sores: "तोंडातील जखमा",
    excessive_salivation: "जास्त लाळ",
    milk_drop: "दूध कमी होणे",
    abnormal_milk: "असामान्य दूध",
    weight_loss: "वजन कमी होणे",
    constipation: "बद्धकोष्ठता",
    tremors: "थरथरणे",
    seizures: "झटके",
    bleeding: "रक्तस्त्राव",
    high_thirst: "जास्त तहान",
    frequent_urination: "वारंवार लघवी",
    reproductive_problem: "प्रजनन समस्या",
    ticks: "गोचीड",
    dehydration: "निर्जलीकरण",
    discharge: "असामान्य स्राव"
  }

};


// =========================================================
// DATA
// =========================================================

const animalOptions = [
  "cow",
  "buffalo",
  "goat",
  "sheep",
  "chicken",
  "duck",
  "pig",
  "dog",
  "cat",
  "horse",
  "donkey",
  "camel",
  "rabbit",
  "turkey",
  "pigeon"
];

const symptomOptions = [
  "fever",
  "cough",
  "diarrhea",
  "vomiting",
  "not_eating",
  "reduced_eating",
  "weakness",
  "lethargy",
  "difficulty_breathing",
  "nasal_discharge",
  "eye_discharge",
  "swelling",
  "skin_lesions",
  "itching",
  "hair_loss",
  "wounds",
  "lameness",
  "abdominal_swelling",
  "bloating",
  "mouth_sores",
  "excessive_salivation",
  "milk_drop",
  "abnormal_milk",
  "weight_loss",
  "constipation",
  "tremors",
  "seizures",
  "bleeding",
  "high_thirst",
  "frequent_urination",
  "reproductive_problem",
  "ticks",
  "dehydration",
  "discharge"
];


// =========================================================
// HELPERS
// =========================================================

function App() {

  const [language, setLanguage] = React.useState(
    localStorage.getItem("pashuraksha_language") ||
    "English"
  );

  const [profile, setProfile] = React.useState(
    null
  );

  const [page, setPage] = React.useState(
    "profile"
  );

  const [reportResult, setReportResult] = React.useState(null);

  const [reports, setReports] = React.useState([]);
  const [appointments, setAppointments] = React.useState([]);
  const [notifications, setNotifications] = React.useState([]);
  const [villages, setVillages] = React.useState([]);
  const [labReports, setLabReports] = React.useState([]);

  const [loading, setLoading] = React.useState(false);

  const [message, setMessage] = React.useState("");

  const [profileForm, setProfileForm] =
    React.useState({
      full_name: "",
      mobile: "",
      role: "Farmer",
      language: language
    });


  function t(key) {

    return (
      translations[language]?.[key] ||
      translations.English?.[key] ||
      key
    );
  }


  function speak(text) {

    if (!window.speechSynthesis) {
      return;
    }

    window.speechSynthesis.cancel();

    const speechLanguage = {
      English: "en-IN",
      Kannada: "kn-IN",
      Hindi: "hi-IN",
      Telugu: "te-IN",
      Tamil: "ta-IN",
      Marathi: "mr-IN"
    };

    const utterance =
      new SpeechSynthesisUtterance(text);

    utterance.lang =
      speechLanguage[language] ||
      "en-IN";

    utterance.rate = 0.9;

    window.speechSynthesis.speak(
      utterance
    );
  }


  function changeLanguage(value) {

    setLanguage(value);

    localStorage.setItem(
      "pashuraksha_language",
      value
    );

    setProfileForm((old) => ({
      ...old,
      language: value
    }));
  }


  async function api(path, options = {}) {

    const response = await fetch(
      `${API}${path}`,
      {
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {})
        },
        ...options
      }
    );

    const data =
      await response.json().catch(
        () => ({})
      );

    if (!response.ok) {
      throw new Error(
        data.detail ||
        t("error")
      );
    }

    return data;
  }


  async function saveProfile(event) {

    event.preventDefault();

    if (!profileForm.full_name.trim()) {
      setMessage(t("fullName"));
      return;
    }

    if (!profileForm.mobile.trim()) {
      setMessage(t("mobile"));
      return;
    }

    try {

      setLoading(true);

      const data =
        await api("/profiles", {
          method: "POST",
          body: JSON.stringify({
            ...profileForm,
            language
          })
        });

      setProfile(data.profile);

      setLanguage(
        data.profile.language
      );

      setPage("portal");

      setMessage(
        t("successProfile")
      );

    } catch (error) {

      setMessage(
        error.message
      );

    } finally {

      setLoading(false);
    }
  }


  async function loadData() {

    if (!profile) return;

    try {

      const [
        reportsData,
        appointmentData,
        notificationData,
        villageData,
        labData
      ] = await Promise.all([

        api(
          `/reports?profile_id=${profile.id}&role=${profile.role}`
        ),

        api(
          `/appointments?profile_id=${profile.id}&role=${profile.role}`
        ),

        api(
          `/notifications/${profile.id}`
        ),

        api("/village-risk"),

        api("/lab-reports")
      ]);

      setReports(
        reportsData.reports || []
      );

      setAppointments(
        appointmentData.appointments || []
      );

      setNotifications(
        notificationData.notifications || []
      );

      setVillages(
        villageData.villages || []
      );

      setLabReports(
        labData.lab_reports || []
      );

    } catch (error) {

      setMessage(
        error.message
      );
    }
  }


  React.useEffect(() => {

    if (profile) {
      loadData();
    }

  }, [profile]);


  function useDemo(role) {

    const data = {

      Farmer: {
        full_name: "Demo Farmer",
        mobile: "9000000001",
        role: "Farmer"
      },

      Veterinary: {
        full_name: "Demo Veterinary",
        mobile: "9000000002",
        role: "Veterinary"
      },

      Government: {
        full_name: "Demo Government",
        mobile: "9000000003",
        role: "Government"
      }

    };

    const selected = data[role];

    setProfileForm({
      ...selected,
      language
    });

    setProfile({
      id:
        role === "Farmer"
          ? 1
          : role === "Veterinary"
            ? 2
            : 3,
      ...selected,
      language
    });

    setPage("portal");
    setMessage("");
  }


  function goProfile() {

    setPage("profile");
  }


  function goPortal() {

    setPage("portal");
  }


  const roleTitle = {

    Farmer: t("farmerPortal"),

    Veterinary:
      t("veterinaryPortal"),

    Government:
      t("governmentPortal")

  };


  return (

    <div className="app-shell">

      <Header
        profile={profile}
        language={language}
        changeLanguage={changeLanguage}
        speak={speak}
        t={t}
        goProfile={goProfile}
      />

      {message && (

        <div className="toast">

          <span>{message}</span>

          <button
            type="button"
            onClick={() =>
              setMessage("")
            }
          >
            ×
          </button>

        </div>

      )}


      {!profile || page === "profile" ? (

        <ProfilePage

          form={profileForm}

          setForm={setProfileForm}

          language={language}

          changeLanguage={changeLanguage}

          onSubmit={saveProfile}

          loading={loading}

          useDemo={useDemo}

          t={t}

          speak={speak}

        />

      ) : (

        <main className="main-content">

          {page === "portal" && (

            <PortalPage
              profile={profile}
              roleTitle={roleTitle[profile.role]}
              setPage={setPage}
              t={t}
              speak={speak}
            />

          )}


          {page === "health" && (

            <HealthPage
              profile={profile}
              t={t}
              api={api}
              goPortal={goPortal}
              setMessage={setMessage}
              setPage={setPage}
              onResult={setReportResult}
              onReportCreated={(report) =>
                setReports((existing) => [
                  report,
                  ...existing.filter(
                    (item) => item.id !== report.id
                  )
                ])
              }
              speak={speak}
            />
          )}
          {page === "result" && (

            <div>
              <PageHeader
                title={t("riskResult")}
                description={t("animalHealthDesc")}
                goPortal={goPortal}
                t={t}
                speak={speak}
              />
              {reportResult && (
                <HealthResult
                  result={reportResult}
                  t={t}
                  speak={speak}
                />
              )}
            </div>
          )}

          {page === "reports" && (

            <ReportsPage
              reports={reports}
              t={t}
              goPortal={goPortal}
              speak={speak}
            />

          )}


          {page === "appointments" && (

            <AppointmentsPage
              profile={profile}
              reports={reports}
              appointments={appointments}
              t={t}
              api={api}
              goPortal={goPortal}
              setMessage={setMessage}
              speak={speak}
            />

          )}


          {page === "notifications" && (

            <NotificationsPage
              notifications={notifications}
              t={t}
              api={api}
              goPortal={goPortal}
              setMessage={setMessage}
              speak={speak}
            />

          )}


          {page === "care" && (

            <CarePage
              t={t}
              goPortal={goPortal}
              speak={speak}
            />

          )}


          {page === "vetReports" && (

            <VetReportsPage
              reports={reports}
              t={t}
              goPortal={goPortal}
              speak={speak}
            />

          )}


          {page === "visits" && (

            <AppointmentRequestsPage
              appointments={appointments}
              profile={profile}
              t={t}
              api={api}
              goPortal={goPortal}
              setMessage={setMessage}
              speak={speak}
            />

          )}


          {page === "laboratory" && (

            <LaboratoryPage
              reports={reports}
              labReports={labReports}
              profile={profile}
              t={t}
              api={api}
              goPortal={goPortal}
              setMessage={setMessage}
              speak={speak}
            />

          )}


          {page === "village" && (

            <VillageRiskPage
              villages={villages}
              t={t}
              goPortal={goPortal}
              speak={speak}
            />

          )}


          {page === "riskMonitoring" && (

            <RiskManagementPage
              villages={villages}
              reports={reports}
              t={t}
              goPortal={goPortal}
              speak={speak}
            />

          )}

        </main>

      )}

    </div>

  );
}


// =========================================================
// HEADER
// =========================================================

function Header({
  profile,
  language,
  changeLanguage,
  speak,
  t,
  goProfile
}) {

  return (

    <header className="topbar">

      <div className="brand">

        <div className="brand-icon">
          🐄
        </div>

        <div>
          <strong>{t("appName")}</strong>

          <span>
            {t("tagline")}
          </span>
        </div>

      </div>


      <div className="top-actions">

        {profile && (

          <button
            className="profile-button"
            onClick={goProfile}
          >
            👤 {profile.full_name}
          </button>

        )}

        <select
          value={language}
          onChange={(event) =>
            changeLanguage(
              event.target.value
            )
          }
          className="language-select"
        >

          <option>English</option>
          <option>Kannada</option>
          <option>Hindi</option>
          <option>Telugu</option>
          <option>Tamil</option>
          <option>Marathi</option>

        </select>

      </div>

    </header>

  );
}


// =========================================================
// PROFILE PAGE
// =========================================================

function ProfilePage({
  form,
  setForm,
  language,
  changeLanguage,
  onSubmit,
  loading,
  useDemo,
  t,
  speak
}) {

  return (

    <main className="profile-page">

      <div className="profile-hero">

        <div className="hero-icon">
          🐄
        </div>

        <div>

          <div className="eyebrow">
            PASHURAKSHA
          </div>

          <h1>
            {t("appName")}
          </h1>

          <p>
            {t("tagline")}
          </p>

        </div>

      </div>


      <div className="profile-grid">

        <section className="profile-card">

          <div className="card-heading">

            <div>
              <h2>{t("profile")}</h2>

              <p>
                Enter your details to open your portal.
              </p>
            </div>

            <button
              className="speak-button"
              type="button"
              onClick={() =>
                speak(
                  `${t("profile")}. ${t("fullName")}. ${t("mobile")}. ${t("role")}. ${t("language")}.`
                )
              }
            >
              {t("readAloud")}
            </button>

          </div>


          <form
            onSubmit={onSubmit}
            className="profile-form"
          >

            <label>

              <span>
                {t("fullName")}
              </span>

              <input
                value={form.full_name}
                onChange={(event) =>
                  setForm({
                    ...form,
                    full_name:
                      event.target.value
                  })
                }
                placeholder={t("fullName")}
              />

            </label>


            <label>

              <span>
                {t("mobile")}
              </span>

              <input
                value={form.mobile}
                onChange={(event) =>
                  setForm({
                    ...form,
                    mobile:
                      event.target.value
                  })
                }
                placeholder="9876543210"
                inputMode="numeric"
              />

            </label>


            <div>
              <div className="field-label">
                {t("role")}
              </div>
              <div className="role-options" role="group" aria-label={t("role")}>
                {[
                  { value: "Farmer", label: t("farmer"), icon: "🌾" },
                  { value: "Veterinary", label: t("veterinary"), icon: "🩺" },
                  { value: "Government", label: t("government"), icon: "🏛️" }
                ].map((option) => (
                  <button
                    className={`role-option ${form.role === option.value ? "selected" : ""}`}
                    type="button"
                    key={option.value}
                    aria-pressed={form.role === option.value}
                    onClick={() =>
                      setForm({
                        ...form,
                        role: option.value
                      })
                    }
                  >
                    <span className="role-option-icon" aria-hidden="true">
                      {option.icon}
                    </span>
                    <span>{t(`${option.value.toLowerCase()}Portal`)}</span>
                  </button>
                ))}
              </div>
            </div>


            <label>

              <span>
                {t("language")}
              </span>

              <select
                value={language}
                onChange={(event) => {

                  changeLanguage(
                    event.target.value
                  );

                  setForm({
                    ...form,
                    language:
                      event.target.value
                  });

                }}
              >

                <option>English</option>
                <option>Kannada</option>
                <option>Hindi</option>
                <option>Telugu</option>
                <option>Tamil</option>
                <option>Marathi</option>

              </select>

            </label>


            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >

              {loading
                ? t("loading")
                : `✓ ${t("save")}`}

            </button>

          </form>

        </section>


        <section className="demo-card">

          <div className="demo-badge">
            {t("demoData")}
          </div>

          <h2>
            {t("demoProfiles")}
          </h2>

          <p>
            {t("demoCredentials")}
          </p>


          <DemoButton
            icon="🌾"
            title={t("farmerDemo")}
            detail={t("demoFarmerDetails")}
            onClick={() =>
              useDemo("Farmer")
            }
          />


          <DemoButton
            icon="🩺"
            title={t("vetDemo")}
            detail={t("demoVetDetails")}
            onClick={() =>
              useDemo("Veterinary")
            }
          />


          <DemoButton
            icon="🏛️"
            title={t("governmentDemo")}
            detail={t("demoGovernmentDetails")}
            onClick={() =>
              useDemo("Government")
            }
          />


          <div className="demo-note">
            Demo data is already stored in
            the SQLite database for presentation.
          </div>

        </section>

      </div>

    </main>

  );
}


function DemoButton({
  icon,
  title,
  detail,
  onClick
}) {

  return (

    <button
      className="demo-button"
      type="button"
      onClick={onClick}
    >

      <span className="demo-icon">
        {icon}
      </span>

      <span className="demo-text">

        <strong>
          {title}
        </strong>

        <small>
          {detail}
        </small>

      </span>

      <span>→</span>

    </button>

  );
}


// =========================================================
// PORTAL
// =========================================================

function PortalPage({
  profile,
  roleTitle,
  setPage,
  t,
  speak
}) {

  const farmerCards = [

    {
      page: "health",
      icon: "🩺",
      title: t("animalHealth"),
      description: t("animalHealthDesc")
    },

    {
      page: "appointments",
      icon: "📅",
      title: t("appointments"),
      description: t("appointmentsDesc")
    },

    {
      page: "reports",
      icon: "📋",
      title: t("reports"),
      description: t("reportsDesc")
    },

    {
      page: "notifications",
      icon: "🔔",
      title: t("notifications"),
      description: t("notificationsDesc")
    },

    {
      page: "care",
      icon: "🌿",
      title: t("animalCare"),
      description: t("animalCareDesc")
    }

  ];


  const vetCards = [

    {
      page: "vetReports",
      icon: "📊",
      title: t("animalReports"),
      description: t("animalReportsDesc")
    },

    {
      page: "visits",
      icon: "🚑",
      title: t("appointmentRequests"),
      description: t("appointmentRequestsDesc")
    },

    {
      page: "laboratory",
      icon: "🔬",
      title: t("laboratory"),
      description: t("laboratoryDesc")
    },

    {
      page: "notifications",
      icon: "🔔",
      title: t("notifications"),
      description: t("notificationsDesc")
    }

  ];


  const governmentCards = [

    {
      page: "vetReports",
      icon: "📋",
      title: t("animalReports"),
      description: t("animalReportsDesc")
    },

    {
      page: "village",
      icon: "🏘️",
      title: t("villageRisk"),
      description: t("villageRiskDesc")
    },

    {
      page: "riskMonitoring",
      icon: "📈",
      title: t("riskManagement"),
      description: t("riskManagementDesc")
    },

    {
      page: "notifications",
      icon: "🔔",
      title: t("notifications"),
      description: t("notificationsDesc")
    }

  ];


  const cards =
    profile.role === "Farmer"
      ? farmerCards
      : profile.role === "Veterinary"
        ? vetCards
        : governmentCards;


  return (

    <div className="portal-page">

      <div className="portal-hero">

        <div>

          <span className="eyebrow">
            {profile.role}
          </span>

          <h1>
            {roleTitle}
          </h1>

          <p>
            {t("welcome")},{" "}
            <strong>
              {profile.full_name}
            </strong>
          </p>

        </div>

        <button
          className="speak-button large"
          type="button"
          onClick={() =>
            speak(
              `${roleTitle}. ${t("welcome")} ${profile.full_name}.`
            )
          }
        >
          {t("readAloud")}
        </button>

      </div>


      <div className="portal-grid">

        {cards.map((card) => (

          <button
            key={card.page}
            className={`portal-card role-${profile.role.toLowerCase()}`}
            type="button"
            onClick={() =>
              setPage(card.page)
            }
          >

            <div className="portal-icon">
              {card.icon}
            </div>

            <div>

              <h3>
                {card.title}
              </h3>

              <p>
                {card.description}
              </p>

            </div>

            <span className="arrow">
              →
            </span>

          </button>

        ))}

      </div>

    </div>

  );
}


// =========================================================
// PAGE HEADER
// =========================================================

function PageHeader({
  title,
  description,
  goPortal,
  t,
  speak
}) {

  return (

    <div className="page-header">

      <button
        className="back-button"
        type="button"
        onClick={goPortal}
      >
        ← {t("backProfile")}
      </button>

      <div className="page-title-row">

        <div>

          <h1>{title}</h1>

          {description && (
            <p>{description}</p>
          )}

        </div>

        <button
          className="speak-button"
          type="button"
          onClick={() =>
            speak(
              `${title}. ${description || ""}`
            )
          }
        >
          {t("readAloud")}
        </button>

      </div>

    </div>

  );
}


// =========================================================
// HEALTH PAGE
// =========================================================

function HealthPage({
  profile,
  t,
  api,
  goPortal,
  setMessage,
  setPage,
  onResult,
  onReportCreated,
  speak
}) {

  const [animalType, setAnimalType] =
    React.useState("");

  const [village, setVillage] =
    React.useState("");

  const [symptoms, setSymptoms] =
    React.useState([]);

  const [daysSick, setDaysSick] =
    React.useState(1);

  const [saving, setSaving] =
    React.useState(false);


  function toggleSymptom(symptom) {

    setSymptoms((old) => {

      if (old.includes(symptom)) {
        return old.filter(
          (item) =>
            item !== symptom
        );
      }

      return [
        ...old,
        symptom
      ];

    });
  }

async function submitReport(event) {
  event.preventDefault();

  if (!animalType) {
    setMessage(t("selectAnimal"));
    return;
  }

  if (!village.trim()) {
    setMessage(t("enterVillage"));
    return;
  }

  if (symptoms.length === 0) {
    setMessage(t("selectSymptoms"));
    return;
  }

  try {
    setSaving(true);

const data = await api("/reports", {
  method: "POST",
  body: JSON.stringify({
    profile_id: profile.id,
    animal_type: animalType,
    village: village.trim(),
    symptoms: symptoms,
    days_sick: Number(daysSick || 0)
  })
});

onReportCreated(data.report);
onResult(data.report);
setPage("result");

  } catch (error) {
    console.error("REPORT ERROR:", error);
    setMessage(error.message);
  } finally {
    setSaving(false);
  }
}

  return (

    <div>

      <PageHeader
        title={t("animalHealth")}
        description={t("animalHealthDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <div className="content-grid">

        <section className="feature-card">

          <form
            className="health-form"
            onSubmit={submitReport}
          >

            <label>

              <span>
                {t("animalType")}
              </span>

              <select
                value={animalType}
                onChange={(event) =>
                  setAnimalType(
                    event.target.value
                  )
                }
              >

                <option value="">
                  {t("selectAnimal")}
                </option>

                {animalOptions.map(
                  (animal) => (

                    <option
                      value={animal}
                      key={animal}
                    >
                      {t(animal)}
                    </option>

                  )
                )}

              </select>

            </label>


            <label>

              <span>
                {t("village")}
              </span>

              <input
                value={village}
                onChange={(event) =>
                  setVillage(
                    event.target.value
                  )
                }
                placeholder={
                  t("enterVillage")
                }
              />

            </label>


            <label>

              <span>
                {t("daysSick")}
              </span>

              <input
                type="number"
                min="0"
                max="365"
                value={daysSick}
                onChange={(event) =>
                  setDaysSick(
                    Math.max(
                      0,
                      Math.min(
                        365,
                        Number(event.target.value) || 0
                      )
                    )
                  )
                }
              />

            </label>


            <div>

              <div className="field-label">
                {t("symptoms")}
              </div>

              <p className="field-help">
                {t("selectSymptoms")}
              </p>


              <div className="symptom-grid">

                {symptomOptions.map(
                  (symptom) => (

                    <label
                      className={`symptom-option ${
                        symptoms.includes(
                          symptom
                        )
                          ? "selected"
                          : ""
                      }`}
                      key={symptom}
                    >

                      <input
                        type="checkbox"
                        checked={symptoms.includes(
                          symptom
                        )}
                        onChange={() =>
                          toggleSymptom(
                            symptom
                          )
                        }
                      />

                      <span>
                        {t(symptom)}
                      </span>

                    </label>

                  )
                )}

              </div>

            </div>


            <button
              className="primary-button"
              type="submit"
              disabled={saving}
            >
              {saving
                ? t("loading")
                : `🩺 ${t("submit")}`}
            </button>

          </form>

        </section>


      </div>

    </div>

  );
}


// =========================================================
// RESULT
// =========================================================

function HealthResult({
  result,
  t,
  speak
}) {

  const riskLevel =
    result.risk_level ||
    result.health_condition ||
    "Unknown";

  const riskScore =
    result.risk_score ?? 0;

  const possibleConditions =
    Array.isArray(result.possible_conditions)
      ? result.possible_conditions
      : result.possible_conditions
        ? [result.possible_conditions]
        : [];

  const careAdvice =
    result.care_advice ||
    result.health_message ||
    "Please consult a veterinarian for proper examination.";

  const levelClass =
    String(riskLevel)
      .toLowerCase()
      .replaceAll(" ", "-");


  return (

    <section className="result-card">

      <div className="result-header">

        <div>

          <span className="eyebrow">
            {t("riskResult")}
          </span>

          <h2>
            {t(result.animal_type) ||
              result.animal_type}
          </h2>

        </div>

        <div
          className={`risk-circle ${levelClass}`}
        >
          {riskScore}
        </div>

      </div>


      <div
        className={`risk-banner ${levelClass}`}
      >

        <strong>
          {riskLevel}
        </strong>

        <span>
          {t("riskScore")}:{" "}
          {riskScore}/100
        </span>

      </div>


      <div className="result-section">

        <h3>
          {t("possibleConditions")}
        </h3>

        <div className="tag-list">

          {possibleConditions.length > 0 ? (

            possibleConditions.map(
              (condition, index) => (

                <span
                  className="tag"
                  key={index}
                >
                  {condition}
                </span>

              )
            )

          ) : (

            <span className="tag">
              No specific condition pattern detected
            </span>

          )}

        </div>

      </div>


      <div className="result-section">

        <h3>
          {t("careAdvice")}
        </h3>

        <p className="care-text">
          {careAdvice}
        </p>

      </div>


      <button
        className="speak-button"
        type="button"
        onClick={() =>
          speak(
            `${riskLevel}. ${careAdvice}`
          )
        }
      >
        {t("readAloud")}
      </button>

    </section>

  );
}


// =========================================================
// REPORTS
// =========================================================

function ReportsPage({
  reports,
  t,
  goPortal,
  speak
}) {

  return (

    <div>

      <PageHeader
        title={t("reports")}
        description={t("reportsDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      {reports.length === 0 ? (

        <EmptyState
          text={t("noReports")}
        />

      ) : (

        <div className="report-list">

          {reports.map((report) => (

            <article
              className="report-card"
              key={report.id}
            >

              <div className="report-animal">
                🐄
              </div>

              <div className="report-main">

                <div className="report-title">

                  <h3>
                    {t(
                      report.animal_type.toLowerCase()
                    ) ||
                      report.animal_type}
                  </h3>

                  <RiskBadge
                    level={
                      report.risk_level
                    }
                  />

                </div>

                <p>
                  📍 {report.village}
                </p>

                <p>
                  📅 {report.days_sick} days
                </p>

                <div className="tag-list">

                  {report.symptoms.map(
                    (symptom) => (

                      <span
                        className="small-tag"
                        key={symptom}
                      >
                        {t(symptom)}
                      </span>

                    )
                  )}

                </div>

              </div>

              {report.is_demo && (

                <span className="demo-label">
                  {t("demoData")}
                </span>

              )}

            </article>

          ))}

        </div>

      )}

    </div>

  );
}


// =========================================================
// APPOINTMENTS
// =========================================================

function AppointmentsPage({
  profile,
  reports,
  appointments,
  t,
  api,
  goPortal,
  setMessage,
  speak
}) {

  const [reportId, setReportId] =
    React.useState("");

  const [date, setDate] =
    React.useState("");

  const [time, setTime] =
    React.useState("");

  const [reason, setReason] =
    React.useState("");


  async function bookAppointment(event) {

    event.preventDefault();

    if (!date || !time || !reason.trim()) {
      setMessage(
        `${t("appointmentDate")}, ${t("appointmentTime")} and ${t("reason")} are required.`
      );
      return;
    }

    try {

      await api("/appointments", {
        method: "POST",
        body: JSON.stringify({
          report_id:
            reportId
              ? Number(reportId)
              : null,

          farmer_profile_id:
            profile.id,

          appointment_date:
            date,

          appointment_time:
            time,

          reason
        })
      });

      setMessage(
        t("successAppointment")
      );

      setReason("");
      setDate("");
      setTime("");
      setReportId("");

      window.location.reload();

    } catch (error) {

      setMessage(
        error.message
      );

    }
  }


  return (

    <div>

      <PageHeader
        title={t("appointments")}
        description={t("appointmentsDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <div className="content-grid">

        <section className="feature-card">

          <h2>
            {t("bookAppointment")}
          </h2>

          <form
            className="health-form"
            onSubmit={bookAppointment}
          >

            <label>

              <span>
                Report
              </span>

              <select
                value={reportId}
                onChange={(event) =>
                  setReportId(
                    event.target.value
                  )
                }
              >

                <option value="">
                  Select report
                </option>

                {reports.map(
                  (report) => (

                    <option
                      key={report.id}
                      value={report.id}
                    >
                      #{report.id}{" "}
                      {report.animal_type}{" "}
                      —{" "}
                      {report.village}
                    </option>

                  )
                )}

              </select>

            </label>


            <label>

              <span>
                {t("appointmentDate")}
              </span>

              <input
                type="date"
                value={date}
                onChange={(event) =>
                  setDate(
                    event.target.value
                  )
                }
              />

            </label>


            <label>

              <span>
                {t("appointmentTime")}
              </span>

              <input
                type="time"
                value={time}
                onChange={(event) =>
                  setTime(
                    event.target.value
                  )
                }
              />

            </label>


            <label>

              <span>
                {t("reason")}
              </span>

              <textarea
                value={reason}
                onChange={(event) =>
                  setReason(
                    event.target.value
                  )
                }
                rows="4"
              />

            </label>


            <button
              className="primary-button"
              type="submit"
            >
              📅 {t("book")}
            </button>

          </form>

        </section>


        <section className="feature-card">

          <h2>
            My Appointments
          </h2>

          {appointments.length === 0 ? (

            <EmptyState
              text={t("noAppointments")}
            />

          ) : (

            <div className="appointment-list">

              {appointments.map(
                (appointment) => (

                  <article
                    className="appointment-card"
                    key={appointment.id}
                  >

                    <div>
                      <strong>
                        {appointment.animal_type ||
                          "Animal"}
                      </strong>

                      <p>
                        📍{" "}
                        {appointment.village ||
                          ""}
                      </p>

                      <p>
                        📅{" "}
                        {appointment.appointment_date}
                        {" "}
                        {appointment.appointment_time}
                      </p>

                      <p>
                        {appointment.reason}
                      </p>

                    </div>

                    <StatusBadge
                      status={
                        appointment.status
                      }
                      t={t}
                    />

                  </article>

                )
              )}

            </div>

          )}

        </section>

      </div>

    </div>

  );
}


// =========================================================
// APPOINTMENT REQUESTS - VET
// =========================================================

function AppointmentRequestsPage({
  appointments,
  profile,
  t,
  api,
  goPortal,
  setMessage,
  speak
}) {

  async function updateStatus(
    appointmentId,
    status
  ) {

    try {

      await api(
        `/appointments/${appointmentId}`,
        {
          method: "PATCH",
          body: JSON.stringify({
            status,
            vet_profile_id:
              profile.id,
            vet_note:
              status === "Approved"
                ? "Appointment approved. Please bring the animal for examination."
                : "Appointment request was not approved."
          })
        }
      );

      setMessage(
        status === "Approved"
          ? t("accept")
          : t("reject")
      );

      window.location.reload();

    } catch (error) {

      setMessage(
        error.message
      );
    }
  }


  return (

    <div>

      <PageHeader
        title={t("appointmentRequests")}
        description={t("appointmentRequestsDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      {appointments.length === 0 ? (

        <EmptyState
          text={t("noAppointments")}
        />

      ) : (

        <div className="request-list">

          {appointments.map(
            (appointment) => (

              <article
                className="request-card"
                key={appointment.id}
              >

                <div className="request-icon">
                  🐄
                </div>

                <div className="request-main">

                  <h3>
                    {appointment.animal_type ||
                      "Animal"}
                  </h3>

                  <p>
                    👤{" "}
                    {appointment.farmer_name ||
                      "Farmer"}
                  </p>

                  <p>
                    📍{" "}
                    {appointment.village ||
                      ""}
                  </p>

                  <p>
                    📅{" "}
                    {appointment.appointment_date}
                    {" "}
                    {appointment.appointment_time}
                  </p>

                  <p>
                    {appointment.reason}
                  </p>

                  <StatusBadge
                    status={
                      appointment.status
                    }
                    t={t}
                  />

                </div>


                {appointment.status ===
                  "Pending" && (

                  <div className="request-actions">

                    <button
                      className="approve-button"
                      type="button"
                      onClick={() =>
                        updateStatus(
                          appointment.id,
                          "Approved"
                        )
                      }
                    >
                      ✓ {t("accept")}
                    </button>

                    <button
                      className="reject-button"
                      type="button"
                      onClick={() =>
                        updateStatus(
                          appointment.id,
                          "Rejected"
                        )
                      }
                    >
                      ✕ {t("reject")}
                    </button>

                  </div>

                )}

              </article>

            )
          )}

        </div>

      )}

    </div>

  );
}


// =========================================================
// LABORATORY
// =========================================================

function LaboratoryPage({
  reports,
  labReports,
  profile,
  t,
  api,
  goPortal,
  setMessage,
  speak
}) {

  const [reportId, setReportId] =
    React.useState("");

  const [result, setResult] =
    React.useState("");

  const [medicine, setMedicine] =
    React.useState("");

  const [followUp, setFollowUp] =
    React.useState(false);

  const [followUpDate, setFollowUpDate] =
    React.useState("");

  const [notes, setNotes] =
    React.useState("");


  async function saveLab(event) {

    event.preventDefault();

    if (!reportId || !result.trim()) {
      setMessage(
        `${t("animalReports")} and ${t("labResult")} are required.`
      );
      return;
    }

    try {

      await api("/lab-reports", {
        method: "POST",
        body: JSON.stringify({
          report_id:
            Number(reportId),

          vet_profile_id:
            profile.id,

          result,

          medicine,

          follow_up_required:
            followUp,

          follow_up_date:
            followUpDate,

          notes
        })
      });

      setMessage(
        t("successLab")
      );

      setReportId("");
      setResult("");
      setMedicine("");
      setFollowUp(false);
      setFollowUpDate("");
      setNotes("");

      window.location.reload();

    } catch (error) {

      setMessage(
        error.message
      );

    }
  }


  return (

    <div>

      <PageHeader
        title={t("laboratory")}
        description={t("laboratoryDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <div className="content-grid">

        <section className="feature-card">

          <h2>
            Add Veterinary Result
          </h2>

          <form
            className="health-form"
            onSubmit={saveLab}
          >

            <label>

              <span>
                Animal Report
              </span>

              <select
                value={reportId}
                onChange={(event) =>
                  setReportId(
                    event.target.value
                  )
                }
              >

                <option value="">
                  Select report
                </option>

                {reports.map(
                  (report) => (

                    <option
                      value={report.id}
                      key={report.id}
                    >
                      #{report.id}{" "}
                      {report.animal_type}{" "}
                      —{" "}
                      {report.village}
                    </option>

                  )
                )}

              </select>

            </label>


            <label>

              <span>
                {t("labResult")}
              </span>

              <textarea
                rows="4"
                value={result}
                onChange={(event) =>
                  setResult(
                    event.target.value
                  )
                }
                placeholder="Enter examination or laboratory result"
              />

            </label>


            <label>

              <span>
                {t("medicine")}
              </span>

              <textarea
                rows="3"
                value={medicine}
                onChange={(event) =>
                  setMedicine(
                    event.target.value
                  )
                }
                placeholder="Enter only veterinarian-prescribed instructions"
              />

            </label>


            <label className="checkbox-line">

              <input
                type="checkbox"
                checked={followUp}
                onChange={(event) =>
                  setFollowUp(
                    event.target.checked
                  )
                }
              />

              <span>
                {t("followUp")}
              </span>

            </label>


            {followUp && (

              <label>

                <span>
                  {t("followUpDate")}
                </span>

                <input
                  type="date"
                  value={followUpDate}
                  onChange={(event) =>
                    setFollowUpDate(
                      event.target.value
                    )
                  }
                />

              </label>

            )}


            <label>

              <span>
                {t("notes")}
              </span>

              <textarea
                rows="3"
                value={notes}
                onChange={(event) =>
                  setNotes(
                    event.target.value
                  )
                }
              />

            </label>


            <button
              className="primary-button"
              type="submit"
            >
              🔬 {t("saveLab")}
            </button>

          </form>

        </section>


        <section className="feature-card">

          <h2>
            Previous Laboratory Reports
          </h2>

          {labReports.length === 0 ? (

            <EmptyState
              text="No laboratory reports."
            />

          ) : (

            <div className="lab-list">

              {labReports.map(
                (lab) => (

                  <article
                    className="lab-card"
                    key={lab.id}
                  >

                    <div className="lab-icon">
                      🔬
                    </div>

                    <div>

                      <h3>
                        {lab.animal_type}
                      </h3>

                      <p>
                        📍 {lab.village}
                      </p>

                      <strong>
                        {lab.result}
                      </strong>

                      {lab.medicine && (

                        <p>
                          💊 {lab.medicine}
                        </p>

                      )}

                      {lab.follow_up_required ? (

                        <span className="follow-up">
                          Follow-up:{" "}
                          {lab.follow_up_date}
                        </span>

                      ) : (

                        <span className="normal-label">
                          {t("normal")}
                        </span>

                      )}

                    </div>

                  </article>

                )
              )}

            </div>

          )}

        </section>

      </div>

    </div>

  );
}


// =========================================================
// VET / GOVERNMENT REPORTS
// =========================================================

function VetReportsPage({
  reports,
  t,
  goPortal,
  speak
}) {

  return (

    <div>

      <PageHeader
        title={t("animalReports")}
        description={t("animalReportsDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <div className="summary-grid">

        <StatCard
          icon="📋"
          value={reports.length}
          label={t("totalReports")}
        />

        <StatCard
          icon="🚨"
          value={
            reports.filter(
              (r) =>
                r.risk_level ===
                  "Critical" ||
                r.risk_level ===
                  "High Concern"
            ).length
          }
          label={t("highCases")}
        />

        <StatCard
          icon="🟢"
          value={
            reports.filter(
              (r) =>
                r.risk_level ===
                  "Mild Concern" ||
                r.risk_level ===
                  "No Significant Risk"
            ).length
          }
          label={t("lowCases")}
        />

      </div>


      <ReportsPage
        reports={reports}
        t={t}
        goPortal={goPortal}
        speak={speak}
      />

    </div>

  );
}


// =========================================================
// VILLAGE RISK
// =========================================================

function VillageRiskPage({
  villages,
  t,
  goPortal,
  speak
}) {

  return (

    <div>

      <PageHeader
        title={t("villageRisk")}
        description={t("villageRiskDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <section className="feature-card">

        <div className="village-grid">

          {villages.map(
            (village) => (

              <article
                className="village-card"
                key={village.village}
              >

                <div className="village-top">

                  <div>

                    <span className="village-icon">
                      🏘️
                    </span>

                    <h3>
                      {village.village}
                    </h3>

                  </div>

                  <RiskBadge
                    level={
                      village.risk_level
                    }
                  />

                </div>


                <div className="village-score">

                  <strong>
                    {village.risk_score}
                  </strong>

                  <span>
                    {t("averageRisk")}
                  </span>

                </div>


                <div className="village-stats">

                  <div>
                    <strong>
                      {village.total_reports}
                    </strong>
                    <span>
                      {t("animalCount")}
                    </span>
                  </div>

                  <div>
                    <strong>
                      {village.high_risk_cases}
                    </strong>
                    <span>
                      {t("highCases")}
                    </span>
                  </div>

                </div>


                <div className="animal-counts">

                  {Object.entries(
                    village.animals || {}
                  ).map(
                    ([animal, count]) => (

                      <span
                        key={animal}
                      >
                        {animal}: {count}
                      </span>

                    )
                  )}

                </div>

              </article>

            )
          )}

        </div>

      </section>

    </div>

  );
}


// =========================================================
// RISK MANAGEMENT
// =========================================================

function RiskManagementPage({
  villages,
  reports,
  t,
  goPortal,
  speak
}) {

  function actionFor(level) {

    if (level === "Critical") {
      return "Immediate veterinary response, field verification and disease-control planning.";
    }

    if (level === "High") {
      return "Increase veterinary visits, monitor affected animals and coordinate local response.";
    }

    if (level === "Medium") {
      return "Continue monitoring, promote preventive care and review new reports.";
    }

    return "Routine monitoring and preventive livestock care.";
  }


  return (

    <div>

      <PageHeader
        title={t("riskManagement")}
        description={t("riskManagementDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <div className="risk-management-hero">

        <div>

          <span className="eyebrow">
            GOVERNMENT MONITORING
          </span>

          <h2>
            {t("riskManagementTitle")}
          </h2>

          <p>
            {reports.length} animal reports
            are currently available for monitoring.
          </p>

        </div>

        <div className="big-number">
          {villages.length}
          <span>
            Villages
          </span>
        </div>

      </div>


      <section className="feature-card">

        <div className="management-list">

          {villages.map(
            (village) => (

              <article
                className="management-card"
                key={village.village}
              >

                <div className="management-main">

                  <h3>
                    🏘️ {village.village}
                  </h3>

                  <p>
                    {village.total_reports} reports •{" "}
                    {village.high_risk_cases} high-risk cases
                  </p>

                </div>


                <RiskBadge
                  level={
                    village.risk_level
                  }
                />


                <div className="management-action">

                  <strong>
                    {t("action")}
                  </strong>

                  <p>
                    {actionFor(
                      village.risk_level
                    )}
                  </p>

                </div>

              </article>

            )
          )}

        </div>

      </section>

    </div>

  );
}


// =========================================================
// NOTIFICATIONS
// =========================================================

function NotificationsPage({
  notifications,
  t,
  api,
  goPortal,
  setMessage,
  speak
}) {

  async function markRead(id) {

    try {

      await api(
        `/notifications/${id}/read`,
        {
          method: "PATCH"
        }
      );

      setMessage(
        "Notification marked as read."
      );

      window.location.reload();

    } catch (error) {

      setMessage(
        error.message
      );

    }
  }


  return (

    <div>

      <PageHeader
        title={t("notifications")}
        description={t("notificationsDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      {notifications.length === 0 ? (

        <EmptyState
          text={t("noNotifications")}
        />

      ) : (

        <div className="notification-list">

          {notifications.map(
            (notification) => (

              <article
                className={`notification-card ${
                  notification.is_read
                    ? "read"
                    : ""
                }`}
                key={notification.id}
              >

                <div className="notification-icon">
                  🔔
                </div>

                <div>

                  <h3>
                    {notification.title}
                  </h3>

                  <p>
                    {notification.message}
                  </p>

                  <small>
                    {notification.created_at}
                  </small>

                </div>

                {!notification.is_read && (

                  <button
                    type="button"
                    className="small-button"
                    onClick={() =>
                      markRead(
                        notification.id
                      )
                    }
                  >
                    ✓
                  </button>

                )}

              </article>

            )
          )}

        </div>

      )}

    </div>

  );
}


// =========================================================
// CARE
// =========================================================

function CarePage({
  t,
  goPortal,
  speak
}) {

  const cards = [

    {
      icon: "💧",
      title: "Dehydration",
      text: "Provide clean water and monitor drinking. Veterinary care may be required if dehydration is severe."
    },

    {
      icon: "🌡️",
      title: "Fever",
      text: "Keep the animal comfortable and monitor its condition. Contact a veterinarian when fever persists or is accompanied by serious symptoms."
    },

    {
      icon: "🫁",
      title: "Breathing Problems",
      text: "Keep the animal calm and in a well-ventilated area. Difficulty breathing can require urgent veterinary attention."
    },

    {
      icon: "🩹",
      title: "Wounds",
      text: "Keep wounds clean and prevent further injury. A veterinarian should examine deep, infected or bleeding wounds."
    },

    {
      icon: "🐛",
      title: "Ticks and Parasites",
      text: "Check the animal regularly and ask a veterinarian about safe parasite-control products."
    },

    {
      icon: "🥬",
      title: "Nutrition",
      text: "Provide suitable food, clean water and a consistent feeding routine. Persistent loss of appetite should be evaluated."
    }

  ];


  return (

    <div>

      <PageHeader
        title={t("animalCare")}
        description={t("animalCareDesc")}
        goPortal={goPortal}
        t={t}
        speak={speak}
      />


      <section className="care-banner">

        <div className="care-banner-icon">
          🌿
        </div>

        <div>

          <h2>
            {t("animalCareTitle")}
          </h2>

          <p>
            Basic supportive care can help while
            arranging appropriate veterinary advice.
          </p>

        </div>

      </section>


      <div className="care-grid">

        {cards.map(
          (card) => (

            <article
              className="care-card"
              key={card.title}
            >

              <div className="care-icon">
                {card.icon}
              </div>

              <h3>
                {card.title}
              </h3>

              <p>
                {card.text}
              </p>

            </article>

          )
        )}

      </div>


      <div className="medical-warning">

        ⚠️

        <strong>
          Veterinary guidance is important for serious,
          persistent or worsening symptoms.
        </strong>

      </div>

    </div>

  );
}


// =========================================================
// SMALL COMPONENTS
// =========================================================

function RiskBadge({ level }) {

  const className =
    String(level || "")
      .toLowerCase()
      .replaceAll(" ", "-");


  return (

    <span
      className={`risk-badge ${className}`}
    >
      {level}
    </span>

  );
}


function StatusBadge({
  status,
  t
}) {

  const translation = {

    Pending: t("pending"),
    Approved: t("approved"),
    Rejected: t("rejected"),
    Completed: t("completed")

  };


  return (

    <span
      className={`status-badge ${String(
        status
      ).toLowerCase()}`}
    >
      {translation[status] ||
        status}
    </span>

  );
}


function StatCard({
  icon,
  value,
  label
}) {

  return (

    <div className="stat-card">

      <span>
        {icon}
      </span>

      <strong>
        {value}
      </strong>

      <p>
        {label}
      </p>

    </div>

  );
}


function EmptyState({
  text
}) {

  return (

    <div className="empty-state">

      <div>
        📭
      </div>

      <p>
        {text}
      </p>

    </div>

  );
}


export default App;