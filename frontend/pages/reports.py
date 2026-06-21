import streamlit as st
import requests
import pandas as pd
from theme import apply_theme
from navbar import show_navbar

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Reports Center", page_icon="📄", layout="wide")
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
st.title("📄 Academic Reports Center")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f8fafc,#eef2ff,#ecfeff);
}
.hero {
    padding:35px;
    border-radius:30px;
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
    margin-bottom:25px;
}
.report-card {
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
<h1>📄 Reports Center</h1>
<p>Generate and download academic performance reports.</p>
</div>
""", unsafe_allow_html=True)

try:
    marks_res = requests.get(f"{API_URL}/marks/all", timeout=5)
    marks_data = marks_res.json().get("marks", [])

    students_res = requests.get(f"{API_URL}/students/all", timeout=5)
    students_data = students_res.json().get("students", [])

except:
    st.error("Backend not connected. Start FastAPI first.")
    st.stop()

c1, c2, c3 = st.columns(3)

c1.metric("Student Records", len(students_data))
c2.metric("Marks Records", len(marks_data))
c3.metric("Report Status", "Ready")

st.markdown("### 📊 Marks Report")

if marks_data:
    df = pd.DataFrame(marks_data)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Marks Report CSV",
        data=csv,
        file_name="student_marks_report.csv",
        mime="text/csv"
    )
else:
    st.info("No marks records found.")

st.markdown("### 🎓 Student Report")

if students_data:
    df2 = pd.DataFrame(students_data)
    st.dataframe(df2, use_container_width=True)

    csv2 = df2.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Student Report CSV",
        data=csv2,
        file_name="student_records_report.csv",
        mime="text/csv"
    )
else:
    st.info("No student records found.")