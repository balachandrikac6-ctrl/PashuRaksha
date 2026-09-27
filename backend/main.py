import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class AnimalReport(BaseModel):
    animal_type: Optional[str] = None
    animal_types: Optional[str] = None
    symptoms: str
    village: str

# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="PashuRaksha API",
    description="Livestock health monitoring and veterinary support system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pashuraksha.db"


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            role TEXT NOT NULL,
            language TEXT NOT NULL DEFAULT 'English',
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animal_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            animal_type TEXT NOT NULL,
            village TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            days_sick INTEGER NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            possible_conditions TEXT NOT NULL,
            care_advice TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            is_demo INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            farmer_profile_id INTEGER NOT NULL,
            vet_profile_id INTEGER,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            vet_note TEXT DEFAULT '',
            is_demo INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            vet_profile_id INTEGER NOT NULL,
            result TEXT NOT NULL,
            medicine TEXT DEFAULT '',
            follow_up_required INTEGER NOT NULL DEFAULT 0,
            follow_up_date TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            notification_type TEXT NOT NULL DEFAULT 'general',
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()

    seed_demo_data(conn)

    conn.close()


# =========================================================
# DEMO DATA
# =========================================================

def seed_demo_data(conn):

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM profiles")
    profile_count = cursor.fetchone()["count"]

    if profile_count > 0:
        return

    now = datetime.now().isoformat(timespec="seconds")

    # Demo profiles
    cursor.execute("""
        INSERT INTO profiles
        (full_name, mobile, role, language, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Demo Farmer",
        "9000000001",
        "Farmer",
        "English",
        now
    ))
    farmer_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO profiles
        (full_name, mobile, role, language, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Demo Veterinary",
        "9000000002",
        "Veterinary",
        "English",
        now
    ))
    vet_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO profiles
        (full_name, mobile, role, language, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Demo Government",
        "9000000003",
        "Government",
        "English",
        now
    ))
    gov_id = cursor.lastrowid

    # Demo report 1
    symptoms1 = [
        "fever",
        "not_eating",
        "weakness",
        "nasal_discharge"
    ]

    score1, level1, conditions1, care1 = calculate_risk(symptoms1, 4)

    cursor.execute("""
        INSERT INTO animal_reports
        (
            profile_id,
            animal_type,
            village,
            symptoms,
            days_sick,
            risk_score,
            risk_level,
            possible_conditions,
            care_advice,
            status,
            is_demo,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        farmer_id,
        "Cow",
        "Rampur",
        json.dumps(symptoms1),
        4,
        score1,
        level1,
        json.dumps(conditions1),
        care1,
        "Submitted",
        1,
        now
    ))

    report1_id = cursor.lastrowid

    # Demo report 2
    symptoms2 = [
        "cough",
        "nasal_discharge"
    ]

    score2, level2, conditions2, care2 = calculate_risk(symptoms2, 3)

    cursor.execute("""
        INSERT INTO animal_reports
        (
            profile_id,
            animal_type,
            village,
            symptoms,
            days_sick,
            risk_score,
            risk_level,
            possible_conditions,
            care_advice,
            status,
            is_demo,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        farmer_id,
        "Buffalo",
        "Rampur",
        json.dumps(symptoms2),
        3,
        score2,
        level2,
        json.dumps(conditions2),
        care2,
        "Submitted",
        1,
        now
    ))

    report2_id = cursor.lastrowid

    # Demo report 3
    symptoms3 = [
        "diarrhea",
        "weakness",
        "reduced_eating"
    ]

    score3, level3, conditions3, care3 = calculate_risk(symptoms3, 2)

    cursor.execute("""
        INSERT INTO animal_reports
        (
            profile_id,
            animal_type,
            village,
            symptoms,
            days_sick,
            risk_score,
            risk_level,
            possible_conditions,
            care_advice,
            status,
            is_demo,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        farmer_id,
        "Goat",
        "Lakshmipur",
        json.dumps(symptoms3),
        2,
        score3,
        level3,
        json.dumps(conditions3),
        care3,
        "Submitted",
        1,
        now
    ))

    report3_id = cursor.lastrowid

    # Demo appointment
    cursor.execute("""
        INSERT INTO appointments
        (
            report_id,
            farmer_profile_id,
            vet_profile_id,
            appointment_date,
            appointment_time,
            reason,
            status,
            vet_note,
            is_demo,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report1_id,
        farmer_id,
        vet_id,
        "2026-09-28",
        "10:30",
        "Fever and weakness",
        "Approved",
        "Please bring the animal for veterinary examination.",
        1,
        now
    ))

    # Notifications
    notifications = [
        (
            farmer_id,
            "Appointment Approved",
            "Your veterinary appointment has been approved for 28 September at 10:30.",
            "appointment"
        ),
        (
            farmer_id,
            "Health Risk Detected",
            "Your cow report has been marked as High Concern. Veterinary review is recommended.",
            "health"
        ),
        (
            vet_id,
            "New Appointment Request",
            "A farmer has submitted a veterinary appointment request.",
            "appointment"
        ),
        (
            gov_id,
            "Village Risk Update",
            "Rampur currently has multiple livestock health reports.",
            "government"
        ),
    ]

    for item in notifications:
        cursor.execute("""
            INSERT INTO notifications
            (
                profile_id,
                title,
                message,
                notification_type,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            item[0],
            item[1],
            item[2],
            item[3],
            now
        ))

    conn.commit()


# =========================================================
# RISK ENGINE
# =========================================================

SYMPTOM_WEIGHTS = {

    "fever": 20,
    "cough": 10,
    "diarrhea": 15,
    "vomiting": 15,
    "not_eating": 20,
    "reduced_eating": 10,
    "weakness": 15,
    "lethargy": 10,
    "difficulty_breathing": 25,
    "nasal_discharge": 10,
    "eye_discharge": 8,
    "swelling": 10,
    "skin_lesions": 12,
    "itching": 7,
    "hair_loss": 6,
    "wounds": 12,
    "lameness": 12,
    "abdominal_swelling": 18,
    "bloating": 18,
    "mouth_sores": 15,
    "excessive_salivation": 12,
    "milk_drop": 10,
    "abnormal_milk": 15,
    "weight_loss": 12,
    "constipation": 8,
    "tremors": 20,
    "seizures": 35,
    "bleeding": 30,
    "high_thirst": 8,
    "frequent_urination": 8,
    "reproductive_problem": 12,
    "ticks": 8,
    "dehydration": 20,
    "discharge": 10,
}


def calculate_risk(symptoms, days_sick):

    score = 0

    for symptom in symptoms:
        score += SYMPTOM_WEIGHTS.get(symptom, 0)

    if days_sick >= 7:
        score += 10
    elif days_sick >= 4:
        score += 5

    score = min(score, 100)

    if score >= 70:
        level = "Critical"
    elif score >= 50:
        level = "High Concern"
    elif score >= 25:
        level = "Moderate Concern"
    elif score > 0:
        level = "Mild Concern"
    else:
        level = "No Significant Risk"

    conditions = []

    symptom_set = set(symptoms)

    if (
        "fever" in symptom_set
        and (
            "cough" in symptom_set
            or "nasal_discharge" in symptom_set
            or "difficulty_breathing" in symptom_set
        )
    ):
        conditions.append("Respiratory illness warning")

    if (
        "diarrhea" in symptom_set
        or "vomiting" in symptom_set
    ):
        conditions.append("Digestive illness / dehydration warning")

    if (
        "skin_lesions" in symptom_set
        or "itching" in symptom_set
        or "hair_loss" in symptom_set
        or "ticks" in symptom_set
    ):
        conditions.append("Skin or external parasite warning")

    if (
        "lameness" in symptom_set
        or "swelling" in symptom_set
        or "wounds" in symptom_set
    ):
        conditions.append("Injury or inflammation warning")

    if (
        "not_eating" in symptom_set
        or "reduced_eating" in symptom_set
        or "weakness" in symptom_set
        or "weight_loss" in symptom_set
    ):
        conditions.append("General illness / nutrition warning")

    if (
        "milk_drop" in symptom_set
        or "abnormal_milk" in symptom_set
    ):
        conditions.append("Milk production / udder health warning")

    if (
        "seizures" in symptom_set
        or "tremors" in symptom_set
    ):
        conditions.append("Neurological warning")

    if not conditions:
        conditions.append("No specific condition pattern detected")

    care = build_care_advice(symptoms, level)

    return score, level, conditions, care


def build_care_advice(symptoms, level):

    advice = []

    advice.append(
        "Provide clean drinking water and keep the animal in a clean, comfortable and shaded area."
    )

    if "diarrhea" in symptoms or "vomiting" in symptoms:
        advice.append(
            "Watch closely for dehydration and contact a veterinarian if symptoms continue or worsen."
        )

    if "difficulty_breathing" in symptoms:
        advice.append(
            "Difficulty breathing can be urgent. Seek veterinary care promptly."
        )

    if "seizures" in symptoms or "bleeding" in symptoms:
        advice.append(
            "This may require urgent veterinary attention."
        )

    if "wounds" in symptoms:
        advice.append(
            "Keep wounds clean and prevent the animal from further injuring the area."
        )

    if "ticks" in symptoms:
        advice.append(
            "Separate the affected animal when appropriate and ask a veterinarian about safe parasite control."
        )

    if level in ["High Concern", "Critical"]:
        advice.append(
            "Veterinary examination is strongly recommended."
        )

    advice.append(
        "Do not give prescription medicines without veterinary guidance."
    )

    return " ".join(advice)


# =========================================================
# MODELS
# =========================================================

class ProfileCreate(BaseModel):
    full_name: str
    mobile: str
    role: str
    language: str = "English"


class ReportCreate(BaseModel):
    profile_id: int
    animal_type: str
    village: str
    symptoms: list[str]
    days_sick: int


class AppointmentCreate(BaseModel):
    report_id: Optional[int] = None
    farmer_profile_id: int
    appointment_date: str
    appointment_time: str
    reason: str


class AppointmentUpdate(BaseModel):
    status: str
    vet_profile_id: int
    vet_note: str = ""


class LabReportCreate(BaseModel):
    report_id: int
    vet_profile_id: int
    result: str
    medicine: str = ""
    follow_up_required: bool = False
    follow_up_date: str = ""
    notes: str = ""


# =========================================================
# BASIC
# =========================================================

@app.get("/")
def root():
    return {
        "success": True,
        "app": "PashuRaksha",
        "message": "PashuRaksha backend is running"
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "status": "healthy",
        "database": str(DB_PATH)
    }


# =========================================================
# PROFILES
# =========================================================

@app.post("/profiles")
def create_profile(profile: ProfileCreate):

    if not profile.full_name.strip():
        raise HTTPException(400, "Full name is required.")

    if not profile.mobile.strip():
        raise HTTPException(400, "Mobile number is required.")

    if profile.role not in ["Farmer", "Veterinary", "Government"]:
        raise HTTPException(400, "Invalid role.")

    allowed_languages = [
        "English",
        "Kannada",
        "Hindi",
        "Telugu",
        "Tamil",
        "Marathi"
    ]

    language = (
        profile.language
        if profile.language in allowed_languages
        else "English"
    )

    conn = get_connection()

    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO profiles
        (full_name, mobile, role, language, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        profile.full_name.strip(),
        profile.mobile.strip(),
        profile.role,
        language,
        now
    ))

    profile_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "success": True,
        "profile_id": profile_id,
        "profile": {
            "id": profile_id,
            "full_name": profile.full_name.strip(),
            "mobile": profile.mobile.strip(),
            "role": profile.role,
            "language": language
        }
    }


@app.get("/profiles/{profile_id}")
def get_profile(profile_id: int):

    conn = get_connection()

    row = conn.execute("""
        SELECT *
        FROM profiles
        WHERE id = ?
    """, (profile_id,)).fetchone()

    conn.close()

    if not row:
        raise HTTPException(404, "Profile not found.")

    return dict(row)


# =========================================================
# REPORTS
# =========================================================

def report_to_dict(row):

    item = dict(row)

    try:
        item["symptoms"] = json.loads(item["symptoms"])
    except Exception:
        item["symptoms"] = []

    try:
        item["possible_conditions"] = json.loads(
            item["possible_conditions"]
        )
    except Exception:
        item["possible_conditions"] = []

    item["is_demo"] = bool(item["is_demo"])

    return item


@app.post("/reports")
def create_report(report: ReportCreate):

    village = report.village.strip()
    if not village:
        raise HTTPException(400, "Please enter village name.")

    if not report.symptoms:
        raise HTTPException(400, "Please select at least one symptom.")

    score, level, conditions, care_advice = calculate_risk(
        report.symptoms,
        report.days_sick
    )
    created_at = datetime.now().isoformat(timespec="seconds")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO animal_reports (
            profile_id,
            animal_type,
            village,
            symptoms,
            days_sick,
            risk_score,
            risk_level,
            possible_conditions,
            care_advice,
            status,
            is_demo,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            report.profile_id,
            report.animal_type,
            village,
            json.dumps(report.symptoms),
            report.days_sick,
            score,
            level,
            json.dumps(conditions),
            care_advice,
            "Submitted",
            0,
            created_at
        )
    )
    report_id = cursor.lastrowid
    conn.commit()
    row = conn.execute(
        "SELECT * FROM animal_reports WHERE id = ?",
        (report_id,)
    ).fetchone()
    conn.close()

    return {
        "success": True,
        "report": report_to_dict(row)
    }


@app.get("/reports")
def get_reports(
    profile_id: Optional[int] = None,
    role: Optional[str] = None
):

    conn = get_connection()

    if role == "Farmer" and profile_id:
        rows = conn.execute(
            """
            SELECT animal_reports.*, profiles.full_name AS farmer_name
            FROM animal_reports
            LEFT JOIN profiles
            ON profiles.id = animal_reports.profile_id
            WHERE animal_reports.profile_id = ?
            ORDER BY animal_reports.id DESC
            """,
            (profile_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT animal_reports.*, profiles.full_name AS farmer_name
            FROM animal_reports
            LEFT JOIN profiles
            ON profiles.id = animal_reports.profile_id
            ORDER BY animal_reports.id DESC
            """
        ).fetchall()

    conn.close()

    return {
        "success": True,
        "reports": [report_to_dict(row) for row in rows]
    }


# =========================================================
# VILLAGE RISK
# =========================================================

@app.get("/village-risk")
def village_risk():

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM animal_reports
        ORDER BY village
    """).fetchall()

    conn.close()

    villages = {}

    for row in rows:

        village = row["village"].strip()

        if village not in villages:
            villages[village] = {
                "village": village,
                "total_reports": 0,
                "high_risk_cases": 0,
                "critical_cases": 0,
                "scores": [],
                "animals": {}
            }

        item = villages[village]

        item["total_reports"] += 1
        item["scores"].append(row["risk_score"])

        if row["risk_level"] == "Critical":
            item["critical_cases"] += 1

        if row["risk_level"] in [
            "Critical",
            "High Concern"
        ]:
            item["high_risk_cases"] += 1

        animal = row["animal_type"]

        item["animals"][animal] = (
            item["animals"].get(animal, 0) + 1
        )

    output = []

    for item in villages.values():

        average = (
            sum(item["scores"]) /
            len(item["scores"])
            if item["scores"]
            else 0
        )

        bonus = min(
            item["total_reports"] * 5,
            25
        )

        village_score = min(
            round(average + bonus),
            100
        )

        if village_score >= 70:
            level = "Critical"
        elif village_score >= 50:
            level = "High"
        elif village_score >= 25:
            level = "Medium"
        else:
            level = "Low"

        output.append({
            "village": item["village"],
            "total_reports": item["total_reports"],
            "high_risk_cases": item["high_risk_cases"],
            "critical_cases": item["critical_cases"],
            "risk_score": village_score,
            "risk_level": level,
            "animals": item["animals"]
        })

    output.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return {
        "success": True,
        "villages": output
    }


# =========================================================
# APPOINTMENTS
# =========================================================

@app.post("/appointments")
def create_appointment(appointment: AppointmentCreate):

    conn = get_connection()

    farmer = conn.execute("""
        SELECT *
        FROM profiles
        WHERE id = ?
    """, (appointment.farmer_profile_id,)).fetchone()

    if not farmer:
        conn.close()
        raise HTTPException(404, "Farmer profile not found.")

    if farmer["role"] != "Farmer":
        conn.close()
        raise HTTPException(
            400,
            "Appointment must be created by a farmer."
        )

    now = datetime.now().isoformat(timespec="seconds")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (
            report_id,
            farmer_profile_id,
            appointment_date,
            appointment_time,
            reason,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        appointment.report_id,
        appointment.farmer_profile_id,
        appointment.appointment_date,
        appointment.appointment_time,
        appointment.reason,
        "Pending",
        now
    ))

    appointment_id = cursor.lastrowid

    vets = conn.execute("""
        SELECT id
        FROM profiles
        WHERE role = 'Veterinary'
    """).fetchall()

    for vet in vets:

        cursor.execute("""
            INSERT INTO notifications
            (
                profile_id,
                title,
                message,
                notification_type,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            vet["id"],
            "New Appointment Request",
            "A farmer has requested a veterinary appointment.",
            "appointment",
            now
        ))

    conn.commit()

    row = conn.execute("""
        SELECT *
        FROM appointments
        WHERE id = ?
    """, (appointment_id,)).fetchone()

    conn.close()

    return {
        "success": True,
        "appointment": dict(row)
    }


@app.get("/appointments")
def get_appointments(
    profile_id: Optional[int] = None,
    role: Optional[str] = None
):

    conn = get_connection()

    if role == "Farmer" and profile_id:

        rows = conn.execute("""
            SELECT
                appointments.*,
                animal_reports.animal_type,
                animal_reports.village
            FROM appointments
            LEFT JOIN animal_reports
            ON animal_reports.id = appointments.report_id
            WHERE appointments.farmer_profile_id = ?
            ORDER BY appointments.id DESC
        """, (profile_id,)).fetchall()

    elif role == "Veterinary":

        rows = conn.execute("""
            SELECT
                appointments.*,
                animal_reports.animal_type,
                animal_reports.village,
                profiles.full_name AS farmer_name
            FROM appointments
            LEFT JOIN animal_reports
            ON animal_reports.id = appointments.report_id
            LEFT JOIN profiles
            ON profiles.id = appointments.farmer_profile_id
            ORDER BY appointments.id DESC
        """).fetchall()

    else:

        rows = conn.execute("""
            SELECT *
            FROM appointments
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return {
        "success": True,
        "appointments": [
            dict(row)
            for row in rows
        ]
    }


@app.patch("/appointments/{appointment_id}")
def update_appointment(
    appointment_id: int,
    update: AppointmentUpdate
):

    allowed = [
        "Approved",
        "Rejected",
        "Completed"
    ]

    if update.status not in allowed:
        raise HTTPException(
            400,
            "Invalid appointment status."
        )

    conn = get_connection()

    vet = conn.execute("""
        SELECT *
        FROM profiles
        WHERE id = ?
    """, (update.vet_profile_id,)).fetchone()

    if not vet or vet["role"] != "Veterinary":
        conn.close()
        raise HTTPException(
            403,
            "Only veterinary users can update appointments."
        )

    appointment = conn.execute("""
        SELECT *
        FROM appointments
        WHERE id = ?
    """, (appointment_id,)).fetchone()

    if not appointment:
        conn.close()
        raise HTTPException(
            404,
            "Appointment not found."
        )

    conn.execute("""
        UPDATE appointments
        SET
            vet_profile_id = ?,
            status = ?,
            vet_note = ?
        WHERE id = ?
    """, (
        update.vet_profile_id,
        update.status,
        update.vet_note,
        appointment_id
    ))

    now = datetime.now().isoformat(timespec="seconds")

    conn.execute("""
        INSERT INTO notifications
        (
            profile_id,
            title,
            message,
            notification_type,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        appointment["farmer_profile_id"],
        f"Appointment {update.status}",
        f"Your veterinary appointment has been {update.status.lower()}.",
        "appointment",
        now
    ))

    conn.commit()

    conn.close()

    return {
        "success": True,
        "message": f"Appointment {update.status.lower()}."
    }


# =========================================================
# LABORATORY
# =========================================================

@app.post("/lab-reports")
def create_lab_report(report: LabReportCreate):

    conn = get_connection()

    vet = conn.execute("""
        SELECT *
        FROM profiles
        WHERE id = ?
    """, (report.vet_profile_id,)).fetchone()

    if not vet or vet["role"] != "Veterinary":
        conn.close()
        raise HTTPException(
            403,
            "Only veterinary users can create lab reports."
        )

    animal_report = conn.execute("""
        SELECT *
        FROM animal_reports
        WHERE id = ?
    """, (report.report_id,)).fetchone()

    if not animal_report:
        conn.close()
        raise HTTPException(
            404,
            "Animal report not found."
        )

    now = datetime.now().isoformat(timespec="seconds")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lab_reports
        (
            report_id,
            vet_profile_id,
            result,
            medicine,
            follow_up_required,
            follow_up_date,
            notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report.report_id,
        report.vet_profile_id,
        report.result,
        report.medicine,
        1 if report.follow_up_required else 0,
        report.follow_up_date,
        report.notes,
        now
    ))

    lab_id = cursor.lastrowid

    cursor.execute("""
        UPDATE animal_reports
        SET status = ?
        WHERE id = ?
    """, (
        "Lab Updated",
        report.report_id
    ))

    cursor.execute("""
        INSERT INTO notifications
        (
            profile_id,
            title,
            message,
            notification_type,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        animal_report["profile_id"],
        "Laboratory Report Updated",
        "Your veterinary laboratory report has been updated.",
        "laboratory",
        now
    ))

    conn.commit()

    row = conn.execute("""
        SELECT *
        FROM lab_reports
        WHERE id = ?
    """, (lab_id,)).fetchone()

    conn.close()

    return {
        "success": True,
        "lab_report": dict(row)
    }


@app.get("/lab-reports")
def get_lab_reports():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            lab_reports.*,
            animal_reports.animal_type,
            animal_reports.village,
            animal_reports.profile_id AS farmer_profile_id
        FROM lab_reports
        JOIN animal_reports
        ON animal_reports.id = lab_reports.report_id
        ORDER BY lab_reports.id DESC
    """).fetchall()

    conn.close()

    return {
        "success": True,
        "lab_reports": [
            dict(row)
            for row in rows
        ]
    }


# =========================================================
# NOTIFICATIONS
# =========================================================

@app.get("/notifications/{profile_id}")
def get_notifications(profile_id: int):

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM notifications
        WHERE profile_id = ?
        ORDER BY id DESC
    """, (profile_id,)).fetchall()

    conn.close()

    return {
        "success": True,
        "notifications": [
            dict(row)
            for row in rows
        ]
    }


@app.patch("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int):

    conn = get_connection()

    conn.execute("""
        UPDATE notifications
        SET is_read = 1
        WHERE id = ?
    """, (notification_id,))

    conn.commit()
    conn.close()

    return {
        "success": True
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():

    conn = get_connection()

    total_reports = conn.execute("""
        SELECT COUNT(*) AS count
        FROM animal_reports
    """).fetchone()["count"]

    critical = conn.execute("""
        SELECT COUNT(*) AS count
        FROM animal_reports
        WHERE risk_level = 'Critical'
    """).fetchone()["count"]

    high = conn.execute("""
        SELECT COUNT(*) AS count
        FROM animal_reports
        WHERE risk_level = 'High Concern'
    """).fetchone()["count"]

    moderate = conn.execute("""
        SELECT COUNT(*) AS count
        FROM animal_reports
        WHERE risk_level = 'Moderate Concern'
    """).fetchone()["count"]

    appointments = conn.execute("""
        SELECT COUNT(*) AS count
        FROM appointments
    """).fetchone()["count"]

    villages = conn.execute("""
        SELECT COUNT(DISTINCT village) AS count
        FROM animal_reports
    """).fetchone()["count"]

    conn.close()

    return {
        "success": True,
        "total_reports": total_reports,
        "critical": critical,
        "high": high,
        "moderate": moderate,
        "appointments": appointments,
        "villages": villages
    }


# =========================================================
# STARTUP
# =========================================================

init_db()