import streamlit as st
import requests
import pandas as pd
import plotly.express as px

from navbar import show_navbar

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Academic Intelligence Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
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

def get_dashboard_stats():
    try:
        res = requests.get(f"{API_URL}/dashboard/stats", timeout=5)
        return res.json()
    except:
        return None

stats = get_dashboard_stats()

if not stats:
    st.error("Backend not connected. Start FastAPI first.")
    st.stop()

total_students = stats.get("total_students", 0)
class_average = stats.get("class_average", 0)
top_score = stats.get("top_score", 0)
risk_students = stats.get("risk_students", 0)
leaderboard = stats.get("leaderboard", [])
grade_distribution = stats.get("grade_distribution", {})
subject_average = stats.get("subject_average", {})

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 35%),
        radial-gradient(circle at top right, rgba(16,185,129,0.14), transparent 35%),
        linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #ecfeff 100%);
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 5rem;
    max-width: 1400px;
}

.top-nav {
    height: 74px;
    padding: 0 28px;
    border-radius: 24px;
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(148,163,184,0.28);
    box-shadow: 0 18px 60px rgba(15,23,42,0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.brand-title {
    font-size: 26px;
    font-weight: 900;
    color: #0f172a;
}

.brand-sub {
    font-size: 13px;
    color: #64748b;
    font-weight: 700;
}

.nav-pill {
    background: #0f172a;
    color: white;
    padding: 12px 18px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 14px;
}

.hero {
    padding: 42px;
    border-radius: 34px;
    background:
        linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.92)),
        radial-gradient(circle at top right, rgba(34,211,238,0.35), transparent 30%);
    color: white;
    box-shadow: 0 30px 90px rgba(15,23,42,0.28);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}

.hero:before {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    background: rgba(34,211,238,0.18);
    border-radius: 50%;
    right: -60px;
    top: -70px;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%,100% { transform: translateY(0px); }
    50% { transform: translateY(18px); }
}

.hero h1 {
    font-size: 50px;
    font-weight: 900;
    margin-bottom: 10px;
    letter-spacing: -1.5px;
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    max-width: 760px;
}

.metric-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 28px;
    padding: 26px;
    box-shadow: 0 20px 55px rgba(15,23,42,0.08);
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 28px 70px rgba(15,23,42,0.14);
}

.metric-label {
    color: #64748b;
    font-size: 14px;
    font-weight: 800;
}

.metric-value {
    color: #0f172a;
    font-size: 38px;
    font-weight: 900;
}

.metric-note {
    color: #10b981;
    font-size: 13px;
    font-weight: 800;
}

.panel {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 30px;
    padding: 28px;
    box-shadow: 0 20px 55px rgba(15,23,42,0.08);
    min-height: 260px;
}

.panel-title {
    font-size: 22px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 12px;
}

.rank-row {
    display: flex;
    justify-content: space-between;
    padding: 14px 0;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    font-weight: 800;
}

.stButton button {
    background: rgba(15,23,42,0.92) !important;
    color: white !important;
    border-radius: 999px !important;
    border: none !important;
    font-weight: 800 !important;
    padding: 0.7rem 1rem !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #06b6d4, #22c55e) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-nav">
    <div>
        <div class="brand-title">Academic Intelligence Hub</div>
        <div class="brand-sub">Student Performance Analysis Dashboard</div>
    </div>
    <div class="nav-pill">Neshika's Workspace</div>
</div>

<div class="hero">
    <h1>Analyze student growth with academic intelligence.</h1>
    <p>A modern performance platform for marks analysis, student ranking, weak subject detection, grade prediction, and AI-powered study recommendations.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Students</div>
        <div class="metric-value">{total_students}</div>
        <div class="metric-note">Live from MongoDB</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Class Average</div>
        <div class="metric-value">{class_average}%</div>
        <div class="metric-note">Overall performance</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top Score</div>
        <div class="metric-value">{top_score}%</div>
        <div class="metric-note">Highest performer</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Risk Students</div>
        <div class="metric-value">{risk_students}</div>
        <div class="metric-note" style="color:#f59e0b;">Needs attention</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

with left:
    st.markdown('<div class="panel-title">Subject Performance Overview</div>', unsafe_allow_html=True)

    if subject_average:
        subject_df = pd.DataFrame({
            "Subject": list(subject_average.keys()),
            "Average": list(subject_average.values())
        })

        fig = px.bar(subject_df, x="Subject", y="Average", text="Average")
        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a"),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No subject data available.")

with right:
    st.markdown('<div class="panel-title">Leaderboard</div>', unsafe_allow_html=True)

    if leaderboard:
        for index, student in enumerate(leaderboard, start=1):
            medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else "⭐"
            st.markdown(f"""
            <div class="rank-row">
                <span>{medal} {student["register_number"]}</span>
                <span>{student["average"]}% | {student["grade"]}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No leaderboard data available.")

st.markdown("<br>", unsafe_allow_html=True)

g1, g2 = st.columns(2)

with g1:
    st.markdown('<div class="panel-title">Grade Distribution</div>', unsafe_allow_html=True)

    if grade_distribution:
        grade_df = pd.DataFrame({
            "Grade": list(grade_distribution.keys()),
            "Students": list(grade_distribution.values())
        })

        fig2 = px.pie(grade_df, names="Grade", values="Students", hole=0.55)
        fig2.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a"),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No grade data available.")

with g2:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">AI Academic Insight</div>
        <p style="color:#64748b;font-weight:700;">Smart summary based on current records.</p>
        <div style="font-size:18px;color:#0f172a;font-weight:800;line-height:1.8;">
            🎯 Class average is currently monitored from live marks data.<br>
            📚 Lowest subject averages can be improved with focused study planning.<br>
            ⚠️ Risk students are automatically identified using performance score.<br>
            🏆 Leaderboard updates dynamically when new marks are added.
        </div>
    </div>
    """, unsafe_allow_html=True)

