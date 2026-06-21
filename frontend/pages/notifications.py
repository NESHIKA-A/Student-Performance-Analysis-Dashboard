import streamlit as st
import requests
from navbar import show_navbar
from theme import apply_theme

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")
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

st.title("🔔 Academic Notification Center")

stats = requests.get(f"{API_URL}/dashboard/stats").json()

st.success(f"🏆 Top Performer: {stats['top_performer']} with {stats['top_score']}%")
st.info(f"📊 Current Class Average: {stats['class_average']}%")
st.warning(f"⚠️ Risk Students: {stats['risk_students']}")

if stats["risk_students"] == 0:
    st.success("✅ No high-risk students currently.")
else:
    st.error("Immediate academic support recommended.")