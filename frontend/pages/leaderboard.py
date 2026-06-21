import streamlit as st
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from navbar import show_navbar

API_URL = "https://student-performance-analysis-dashboard.onrender.com"

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")
show_navbar()

st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    padding: 35px;
    border-radius: 28px;
    color: white;
    margin-bottom: 25px;
}
.rank-card {
    background: white;
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 15px 45px rgba(15,23,42,0.08);
}
.rank-title {
    font-size: 22px;
    font-weight: 900;
    color: #0f172a;
}
.rank-detail {
    font-size: 16px;
    font-weight: 700;
    color: #334155;
    line-height: 1.8;
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
    res = requests.get(f"{API_URL}/dashboard/stats", timeout=10)
    stats = res.json()
except Exception as e:
    st.error(f"Backend connection failed: {e}")
    st.stop()

leaderboard = stats.get("leaderboard", [])

if not leaderboard:
    st.info("No leaderboard data found. Add marks first.")
    st.stop()

top = leaderboard[0]

st.success(
    f"🏆 Top Performer: {top['register_number']} | "
    f"{top['average']}% | Grade {top['grade']}"
)

st.subheader("🥇 Top Rankings")

for index, student in enumerate(leaderboard, start=1):
    medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else "⭐"

    st.markdown(f"""
    <div class="rank-card">
        <div class="rank-title">{medal} Rank #{index}</div>
        <div class="rank-detail">
            Register No: {student.get("register_number", "N/A")}<br>
            Average: {student.get("average", 0)}%<br>
            Grade: {student.get("grade", "N/A")}<br>
            Risk Level: {student.get("risk_level", "N/A")}
        </div>
    </div>
    """, unsafe_allow_html=True)