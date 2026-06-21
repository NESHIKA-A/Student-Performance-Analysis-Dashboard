import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from navbar import show_navbar
from theme import apply_theme

API_URL = "https://student-performance-analysis-dashboard.onrender.com"

st.set_page_config(page_title="Performance Trends", page_icon="📈", layout="wide")
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

st.title("📈 Performance Trends")

marks = requests.get(f"{API_URL}/marks/all").json().get("marks", [])

if not marks:
    st.info("No marks data found.")
    st.stop()

df = pd.DataFrame([
    {
        "Register Number": m["register_number"],
        "Average": m["average"],
        "Grade": m["grade"],
        "Risk Level": m["risk_level"]
    }
    for m in marks
])

fig = px.line(
    df,
    x="Register Number",
    y="Average",
    markers=True,
    title="Student Average Performance Trend"
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(
    df,
    x="Register Number",
    y="Average",
    color="Grade",
    title="Student Performance Comparison"
)

st.plotly_chart(fig2, use_container_width=True)

st.dataframe(df, use_container_width=True)
