import streamlit as st
import requests
from navbar import show_navbar
from theme import apply_theme

API_URL = "https://student-performance-analysis-dashboard.onrender.com"

st.set_page_config(page_title="Admin Dashboard", page_icon="👨‍💼", layout="wide")
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

st.title("👨‍💼 Admin Control Center")

stats = requests.get(f"{API_URL}/dashboard/stats").json()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", stats["total_students"])
c2.metric("Class Average", f"{stats['class_average']}%")
c3.metric("Top Score", f"{stats['top_score']}%")
c4.metric("Risk Students", stats["risk_students"])

st.subheader("System Overview")

st.write("✅ Backend: FastAPI")
st.write("✅ Database: MongoDB Atlas")
st.write("✅ Frontend: Streamlit")
st.write("✅ AI: Gemini Academic Advisor")
st.write("✅ Reports: CSV + PDF Export")
