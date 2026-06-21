import streamlit as st
import requests
from navbar import show_navbar
from theme import apply_theme

API_URL = "https://student-performance-analysis-dashboard.onrender.com"

st.set_page_config(
    page_title="AI Academic Advisor",
    page_icon="🤖",
    layout="wide"
)
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
    background: linear-gradient(135deg,#f8fafc,#eef2ff,#ecfeff);
}
.hero {
    padding:35px;
    border-radius:30px;
    background:linear-gradient(135deg,#111827,#1e293b);
    color:white;
    margin-bottom:20px;
}
.card {
    background:white;
    border-radius:25px;
    padding:25px;
    box-shadow:0 15px 40px rgba(15,23,42,0.08);
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🤖 AI Academic Advisor</h1>
<p>Generate real Gemini-powered study plans from MongoDB student marks.</p>
</div>
""", unsafe_allow_html=True)

students = requests.get(f"{API_URL}/students/all").json().get("students", [])
marks = requests.get(f"{API_URL}/marks/all").json().get("marks", [])

reg_numbers = [s["register_number"] for s in students]

selected = st.selectbox("Select Student Register Number", reg_numbers)

student = next((s for s in students if s["register_number"] == selected), None)
mark = next((m for m in marks if m["register_number"] == selected), None)

if student and mark:
    st.markdown(f"""
    <div class="card">
        <h3>👤 Selected Student</h3>
        <b>Name:</b> {student["name"]}<br>
        <b>Register Number:</b> {student["register_number"]}<br>
        <b>Department:</b> {student["department"]}<br>
        <b>Average:</b> {mark["average"]}%<br>
        <b>Grade:</b> {mark["grade"]}<br>
        <b>Risk Level:</b> {mark["risk_level"]}<br>
        <b>Weak Subjects:</b> {", ".join(mark["weak_subjects"]) if mark["weak_subjects"] else "None"}<br>
        <b>Strong Subjects:</b> {", ".join(mark["strong_subjects"]) if mark["strong_subjects"] else "None"}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🤖 Generate Gemini Study Plan"):
        payload = {
            "student_name": student["name"],
            "average": mark["average"],
            "grade": mark["grade"],
            "risk_level": mark["risk_level"],
            "weak_subjects": mark["weak_subjects"],
            "strong_subjects": mark["strong_subjects"]
        }

        with st.spinner("Gemini is generating a personalized academic plan..."):
            res = requests.post(f"{API_URL}/ai/study-plan", json=payload)
            data = res.json()

        if data.get("success"):
            st.markdown("### 🎯 AI Generated Study Plan")
            st.markdown(data["ai_response"])
        else:
            st.error(data.get("message"))
else:
    st.warning("Student marks not found. Add marks first.")
