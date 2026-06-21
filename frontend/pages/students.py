import streamlit as st
import requests
import pandas as pd
from navbar import show_navbar
from theme import apply_theme


API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Student Directory", page_icon="🎓", layout="wide")
apply_theme()
show_navbar()

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #eef2ff, #ecfeff);
}
.block-container {
    padding-top: 1.2rem;
    max-width: 1400px;
}
.hero-box {
    padding: 34px;
    border-radius: 30px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    box-shadow: 0 25px 70px rgba(15,23,42,0.25);
    margin-bottom: 25px;
}
.hero-box h1 {
    font-size: 42px;
    font-weight: 900;
}
.student-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(148,163,184,0.28);
    border-radius: 26px;
    padding: 24px;
    box-shadow: 0 18px 50px rgba(15,23,42,0.08);
    margin-bottom: 18px;
    transition: 0.25s ease;
}
.student-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 26px 70px rgba(15,23,42,0.14);
}
.student-name {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a;
}
.student-meta {
    color: #64748b;
    font-weight: 700;
    margin-top: 4px;
}
.badge {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 999px;
    background: #e0f2fe;
    color: #0369a1;
    font-weight: 900;
    font-size: 13px;
    margin-top: 12px;
}
.form-panel {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 28px;
    padding: 26px;
    box-shadow: 0 20px 55px rgba(15,23,42,0.08);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <h1>🎓 Student Directory</h1>
    <p style="font-size:18px;color:#cbd5e1;font-weight:600;">
        Manage student profiles, departments, semester details and academic identity records.
    </p>
</div>
""", unsafe_allow_html=True)

try:
    res = requests.get(f"{API_URL}/students/all", timeout=5)
    students = res.json().get("students", [])
except:
    students = []
    st.error("Backend not connected. Start FastAPI first.")

top1, top2, top3 = st.columns(3)
top1.metric("Total Students", len(students))
top2.metric("Departments", len(set([s["department"] for s in students])) if students else 0)
top3.metric("Active Records", len(students))

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([0.9, 1.4])

with left:
    st.markdown('<div class="form-panel">', unsafe_allow_html=True)
    st.subheader("➕ Add New Student")

    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        register_number = st.text_input("Register Number")
        department = st.selectbox("Department", ["CSE", "IT", "ECE", "CCE", "CSBS", "AIML", "AIDS"])
        year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        semester = st.selectbox("Semester", ["1", "2", "3", "4", "5", "6", "7", "8"])
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            data = {
                "name": name,
                "register_number": register_number,
                "department": department,
                "year": year,
                "semester": semester,
                "email": email,
                "phone": phone
            }

            response = requests.post(f"{API_URL}/students/add", json=data)
            result = response.json()

            if result.get("success"):
                st.success("Student added successfully")
                st.rerun()
            else:
                st.error(result.get("message"))

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.subheader("📚 Student Records")

    search = st.text_input("Search by name, register number or department")

    filtered = students
    if search:
        filtered = [
            s for s in students
            if search.lower() in s["name"].lower()
            or search.lower() in s["register_number"].lower()
            or search.lower() in s["department"].lower()
        ]

    if filtered:
        for s in filtered:
            st.markdown(f"""
            <div class="student-card">
                <div class="student-name">👤 {s["name"]}</div>
                <div class="student-meta">{s["department"]} • {s["year"]} • Semester {s["semester"]}</div>
                <div class="badge">Reg No: {s["register_number"]}</div>
                <p style="margin-top:14px;color:#475569;font-weight:700;">
                    📧 {s["email"]}<br>
                    📱 {s["phone"]}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No students found.")

st.markdown("---")

if students:
    st.subheader("📋 Table View")
    df = pd.DataFrame(students)
    st.dataframe(df, use_container_width=True)