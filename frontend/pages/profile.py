import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from theme import apply_theme
from navbar import show_navbar

API_URL = "https://student-performance-analysis-dashboard.onrender.com"

st.set_page_config(page_title="Student Profile", page_icon="👤", layout="wide")
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

st.title("👤 Student Performance Profile")

students = requests.get(f"{API_URL}/students/all").json().get("students", [])
marks = requests.get(f"{API_URL}/marks/all").json().get("marks", [])

reg_numbers = [s["register_number"] for s in students]

selected = st.selectbox("Select Register Number", reg_numbers)

student = next((s for s in students if s["register_number"] == selected), None)
mark = next((m for m in marks if m["register_number"] == selected), None)

if student:
    st.subheader(student["name"])
    st.write(f"Department: {student['department']}")
    st.write(f"Year: {student['year']} | Semester: {student['semester']}")
    st.write(f"Email: {student['email']}")
    st.write(f"Phone: {student['phone']}")

if mark:
    c1, c2, c3 = st.columns(3)
    c1.metric("Average", f"{mark['average']}%")
    c2.metric("Grade", mark["grade"])
    c3.metric("Risk", mark["risk_level"])

    df = pd.DataFrame({
        "Subject": list(mark["subjects"].keys()),
        "Marks": list(mark["subjects"].values())
    })

    fig = px.bar(df, x="Subject", y="Marks", text="Marks")
    st.plotly_chart(fig, use_container_width=True)

    st.warning("Weak Subjects: " + (", ".join(mark["weak_subjects"]) if mark["weak_subjects"] else "None"))
    st.success("Strong Subjects: " + (", ".join(mark["strong_subjects"]) if mark["strong_subjects"] else "None"))
else:
    st.info("No marks found for this student.")
