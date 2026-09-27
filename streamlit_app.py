from datetime import date, time

import streamlit as st

from backend import main as api


ANIMALS = [
    "cow", "buffalo", "goat", "sheep", "chicken", "duck", "pig",
    "dog", "cat", "horse", "donkey", "camel", "rabbit", "turkey", "pigeon"
]

SYMPTOMS = [
    "fever", "cough", "diarrhea", "vomiting", "not_eating",
    "reduced_eating", "weakness", "lethargy", "difficulty_breathing",
    "nasal_discharge", "eye_discharge", "swelling", "skin_lesions",
    "itching", "hair_loss", "wounds", "lameness", "abdominal_swelling",
    "bloating", "mouth_sores", "excessive_salivation", "milk_drop",
    "abnormal_milk", "weight_loss", "constipation", "tremors", "seizures",
    "bleeding", "high_thirst", "frequent_urination", "reproductive_problem",
    "ticks", "dehydration", "discharge"
]

ROLES = ["Farmer", "Veterinary", "Government"]

st.set_page_config(
    page_title="PashuRaksha",
    page_icon="🐄",
    layout="wide"
)


def label(value):
    return str(value or "").replace("_", " ").title()


def profiles_for_role(role):
    conn = api.get_connection()
    rows = conn.execute(
        "SELECT id, full_name, mobile, role FROM profiles WHERE role = ? ORDER BY id DESC",
        (role,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def report_rows(profile):
    return api.get_reports(
        profile_id=profile["id"],
        role=profile["role"]
    )["reports"]


def show_risk(report):
    st.subheader(f"{label(report['animal_type'])} health risk")
    score_col, level_col, location_col = st.columns(3)
    score_col.metric("Risk score", f"{report['risk_score']}/100")
    level_col.metric("Risk level", report["risk_level"])
    location_col.metric("Village", report["village"])
    conditions = report.get("possible_conditions") or []
    st.markdown("**Possible warning patterns**")
    st.write(" · ".join(conditions) if conditions else "No specific pattern detected")
    st.markdown("**Care recommendations**")
    st.write(report.get("care_advice") or "Consult a veterinarian for an examination.")


def show_overview(profile, reports):
    overview = api.dashboard()
    st.title(f"{profile['role']} portal")
    st.caption(f"Welcome, {profile['full_name']}")
    columns = st.columns(4)
    columns[0].metric("Health reports", overview["total_reports"])
    columns[1].metric("Critical cases", overview["critical"])
    columns[2].metric("Appointments", overview["appointments"])
    columns[3].metric("Villages monitored", overview["villages"])
    st.subheader("Recent reports")
    if reports:
        for report in reports[:5]:
            with st.container(border=True):
                cols = st.columns([2, 2, 2, 1])
                cols[0].write(f"**{label(report['animal_type'])}**")
                cols[1].write(report["village"])
                cols[2].write(report["risk_level"])
                cols[3].write(f"{report['risk_score']}/100")
    else:
        st.info("No reports available yet.")


def farmer_health_check(profile):
    st.title("Animal health check")
    with st.form("health_report_form"):
        animal = st.selectbox("Animal type", ANIMALS, format_func=label)
        village = st.text_input("Village")
        days_sick = st.number_input("Days unwell", min_value=0, max_value=365, value=1)
        symptoms = st.multiselect("Observed symptoms", SYMPTOMS, format_func=label)
        submitted = st.form_submit_button("Submit report", type="primary")

    if submitted:
        if not village.strip():
            st.error("Enter the village name.")
        elif not symptoms:
            st.error("Select at least one symptom.")
        else:
            result = api.create_report(api.ReportCreate(
                profile_id=profile["id"],
                animal_type=animal,
                village=village.strip(),
                symptoms=symptoms,
                days_sick=int(days_sick)
            ))["report"]
            st.session_state["latest_report"] = result
            st.success("Report saved. Risk prediction is ready.")

    latest = st.session_state.get("latest_report")
    if latest and latest.get("profile_id") == profile["id"]:
        show_risk(latest)


def farmer_reports(profile):
    st.title("My health reports")
    reports = report_rows(profile)
    if not reports:
        st.info("No reports available yet.")
        return
    for report in reports:
        with st.expander(
            f"#{report['id']} · {label(report['animal_type'])} · {report['village']} · {report['risk_level']}"
        ):
            show_risk(report)
            st.write("Symptoms: " + ", ".join(label(item) for item in report["symptoms"]))
            st.caption(f"Submitted {report['created_at']}")


def farmer_appointments(profile):
    st.title("Appointments")
    reports = report_rows(profile)
    report_by_id = {item["id"]: item for item in reports}

    with st.form("appointment_form"):
        report_id = st.selectbox(
            "Health report",
            [None, *report_by_id],
            format_func=lambda item_id: (
                "No report selected" if item_id is None else
                f"#{item_id} · {label(report_by_id[item_id]['animal_type'])} · {report_by_id[item_id]['village']}"
            )
        )
        appointment_date = st.date_input("Appointment date", value=date.today())
        appointment_time = st.time_input("Appointment time", value=time(9, 0))
        reason = st.text_area("Reason")
        submitted = st.form_submit_button("Request appointment", type="primary")

    if submitted:
        if not reason.strip():
            st.error("Enter a reason for the appointment.")
        else:
            api.create_appointment(api.AppointmentCreate(
                report_id=report_id,
                farmer_profile_id=profile["id"],
                appointment_date=appointment_date.isoformat(),
                appointment_time=appointment_time.strftime("%H:%M"),
                reason=reason.strip()
            ))
            st.success("Appointment request submitted.")

    appointments = api.get_appointments(
        profile_id=profile["id"],
        role="Farmer"
    )["appointments"]
    st.subheader("Your requests")
    if not appointments:
        st.info("No appointments available.")
    for item in appointments:
        with st.container(border=True):
            st.write(f"**{item.get('animal_type') or 'Appointment'}** · {item['status']}")
            st.write(f"{item['appointment_date']} at {item['appointment_time']}")
            st.write(item["reason"])


def all_reports():
    return api.get_reports(role="Veterinary")["reports"]


def veterinary_reports():
    st.title("Animal reports")
    reports = all_reports()
    if not reports:
        st.info("No reports available.")
        return
    high_risk = sum(item["risk_level"] in ("Critical", "High Concern") for item in reports)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total reports", len(reports))
    col2.metric("High-risk cases", high_risk)
    col3.metric("Villages", len({item["village"] for item in reports}))
    for report in reports:
        with st.expander(
            f"#{report['id']} · {label(report['animal_type'])} · {report['village']} · {report['risk_level']}"
        ):
            show_risk(report)
            st.write("Symptoms: " + ", ".join(label(item) for item in report["symptoms"]))
            st.write(f"Farmer: {report.get('farmer_name') or 'Farmer'}")


def veterinary_appointments(profile):
    st.title("Appointment requests")
    appointments = api.get_appointments(
        profile_id=profile["id"],
        role="Veterinary"
    )["appointments"]
    if not appointments:
        st.info("No appointment requests.")
        return

    for item in appointments:
        with st.container(border=True):
            st.write(f"### {label(item.get('animal_type') or 'Animal')} · {item['status']}")
            st.write(f"Farmer: {item.get('farmer_name') or 'Farmer'} · {item.get('village') or ''}")
            st.write(f"{item['appointment_date']} at {item['appointment_time']}")
            st.write(item["reason"])
            if item["status"] == "Pending":
                left, right, _ = st.columns([1, 1, 5])
                if left.button("Approve", key=f"approve_{item['id']}"):
                    api.update_appointment(item["id"], api.AppointmentUpdate(
                        status="Approved",
                        vet_profile_id=profile["id"],
                        vet_note="Appointment approved. Please bring the animal for examination."
                    ))
                    st.rerun()
                if right.button("Reject", key=f"reject_{item['id']}"):
                    api.update_appointment(item["id"], api.AppointmentUpdate(
                        status="Rejected",
                        vet_profile_id=profile["id"],
                        vet_note="Appointment request was not approved."
                    ))
                    st.rerun()


def veterinary_laboratory(profile):
    st.title("Laboratory")
    reports = all_reports()
    if not reports:
        st.info("No animal reports are available to examine.")
        return
    report_by_id = {item["id"]: item for item in reports}

    with st.form("lab_report_form"):
        report_id = st.selectbox(
            "Animal report",
            list(report_by_id),
            format_func=lambda item_id: (
                f"#{item_id} · {label(report_by_id[item_id]['animal_type'])} · "
                f"{report_by_id[item_id]['village']} · {report_by_id[item_id]['risk_level']}"
            )
        )
        result = st.text_area("Examination / laboratory result")
        medicine = st.text_area("Veterinary medicine / instructions")
        follow_up = st.checkbox("Follow-up required")
        follow_up_date = st.date_input("Follow-up date") if follow_up else None
        notes = st.text_area("Veterinary notes")
        submitted = st.form_submit_button("Save laboratory report", type="primary")

    if submitted:
        if not result.strip():
            st.error("Enter an examination or laboratory result.")
        else:
            api.create_lab_report(api.LabReportCreate(
                report_id=report_id,
                vet_profile_id=profile["id"],
                result=result.strip(),
                medicine=medicine.strip(),
                follow_up_required=follow_up,
                follow_up_date=follow_up_date.isoformat() if follow_up_date else "",
                notes=notes.strip()
            ))
            st.success("Laboratory report saved.")

    st.subheader("Previous laboratory reports")
    labs = api.get_lab_reports()["lab_reports"]
    if not labs:
        st.info("No laboratory reports available.")
    for lab in labs:
        with st.container(border=True):
            st.write(f"**#{lab['report_id']} · {label(lab['animal_type'])} · {lab['village']}**")
            st.write(lab["result"])
            if lab.get("medicine"):
                st.write("Instructions: " + lab["medicine"])
            if lab["follow_up_required"]:
                st.caption("Follow-up: " + (lab.get("follow_up_date") or "Date not set"))


def village_risk():
    st.title("Village risk")
    villages = api.village_risk()["villages"]
    if not villages:
        st.info("No village reports available.")
        return
    st.dataframe(
        [
            {
                "Village": item["village"],
                "Reports": item["total_reports"],
                "High-risk cases": item["high_risk_cases"],
                "Risk score": item["risk_score"],
                "Risk level": item["risk_level"]
            }
            for item in villages
        ],
        use_container_width=True,
        hide_index=True
    )


st.title("PashuRaksha")
st.caption("Livestock health and veterinary support")

with st.sidebar:
    st.header("Portal")
    role = st.selectbox("Choose a portal", ROLES)
    with st.expander("Create a profile"):
        with st.form("profile_form"):
            full_name = st.text_input("Full name")
            mobile = st.text_input("Mobile number", max_chars=15)
            language = st.selectbox(
                "Language",
                ["English", "Kannada", "Hindi", "Telugu", "Tamil", "Marathi"]
            )
            create_profile = st.form_submit_button("Create profile")
        if create_profile:
            if not full_name.strip() or not mobile.strip():
                st.error("Enter a name and mobile number.")
            else:
                api.create_profile(api.ProfileCreate(
                    full_name=full_name.strip(),
                    mobile=mobile.strip(),
                    role=role,
                    language=language
                ))
                st.rerun()

    profiles = profiles_for_role(role)
    if not profiles:
        st.info("Create a profile to open this portal.")
        st.stop()

    profile_by_id = {item["id"]: item for item in profiles}
    selected_profile_id = st.selectbox(
        "Profile",
        list(profile_by_id),
        format_func=lambda item_id: (
            f"{profile_by_id[item_id]['full_name']} · {profile_by_id[item_id]['mobile']}"
        ),
        key=f"profile_{role}"
    )

profile = profile_by_id[selected_profile_id]
reports = report_rows(profile)

pages = {
    "Farmer": ["Overview", "Health check", "My reports", "Appointments", "Animal care"],
    "Veterinary": ["Overview", "Animal reports", "Appointment requests", "Laboratory"],
    "Government": ["Overview", "Animal reports", "Village risk"]
}
page = st.sidebar.radio("Go to", pages[role])

if page == "Overview":
    show_overview(profile, reports)
elif page == "Health check":
    farmer_health_check(profile)
elif page == "My reports" or page == "Animal reports":
    if role == "Farmer":
        farmer_reports(profile)
    else:
        veterinary_reports()
elif page == "Appointments":
    farmer_appointments(profile)
elif page == "Appointment requests":
    veterinary_appointments(profile)
elif page == "Laboratory":
    veterinary_laboratory(profile)
elif page == "Village risk":
    village_risk()
elif page == "Animal care":
    st.title("Animal care")
    st.info("Provide clean water and a clean, shaded resting area. Contact a veterinarian for serious, persistent, or worsening symptoms. Do not give prescription medicines without veterinary guidance.")