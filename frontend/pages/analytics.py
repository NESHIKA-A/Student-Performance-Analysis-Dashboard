import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from navbar import show_navbar

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)
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

st.title("📊 Performance Analytics")

try:
    stats = requests.get(f"{API_URL}/dashboard/stats").json()

    subject_average = stats["subject_average"]
    grade_distribution = stats["grade_distribution"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Subject Performance")

        df = pd.DataFrame({
            "Subject": list(subject_average.keys()),
            "Average": list(subject_average.values())
        })

        fig = px.bar(
            df,
            x="Subject",
            y="Average",
            text="Average"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Grade Distribution")

        df2 = pd.DataFrame({
            "Grade": list(grade_distribution.keys()),
            "Students": list(grade_distribution.values())
        })

        fig2 = px.pie(
            df2,
            names="Grade",
            values="Students",
            hole=0.5
        )

        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")