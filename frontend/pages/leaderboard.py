import streamlit as st
import requests
import pandas as pd
from theme import apply_theme
from navbar import show_navbar

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
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
    margin-bottom:25px;
}
.rank-card {
    background:white;
    border-radius:25px;
    padding:20px;
    margin-bottom:12px;
    box-shadow:0 15px 40px rgba(15,23,42,0.08);
}
.rank-name {
    font-size:22px;
    font-weight:900;
    color:#0f172a;
}
.rank-score {
    font-size:28px;
    font-weight:900;
    color:#2563eb;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🏆 Academic Leaderboard</h1>
<p>Top performing students ranked by academic average.</p>
</div>
""", unsafe_allow_html=True)

try:
    stats = requests.get(
        f"{API_URL}/dashboard/stats",
        timeout=5
    ).json()

    leaderboard = stats["leaderboard"]

except:
    st.error("Backend not connected.")
    st.stop()

if leaderboard:

    first = leaderboard[0]

    st.success(
        f"🥇 Top Performer: {first['register_number']} | "
        f"{first['average']}% | Grade {first['grade']}"
    )

    st.markdown("### 🏅 Top Rankings")

    for idx, student in enumerate(leaderboard, start=1):

        medal = "⭐"

        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"

        st.markdown(f"""
        <div class="rank-card">
            <div class="rank-name">
                {medal} Rank #{idx}
            </div>

            <br>

            Register No:
            <b>{student['register_number']}</b>

            <br><br>

            Grade:
            <b>{student['grade']}</b>

            <br><br>

            Risk Level:
            <b>{student['risk_level']}</b>

            <div class="rank-score">
                {student['average']}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📋 Leaderboard Table")

    df = pd.DataFrame(leaderboard)

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info("No leaderboard data found.")