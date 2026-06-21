import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from theme import apply_theme
from navbar import show_navbar
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Marks Intelligence", page_icon="📝", layout="wide")
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
    background: linear-gradient(135deg, #f8fafc, #eef2ff, #ecfeff);
}
.block-container {
    padding-top: 1.2rem;
    max-width: 1400px;
}
.hero-box {
    padding: 34px;
    border-radius: 30px;
    background: linear-gradient(135deg, #111827, #1e293b);
    color: white;
    box-shadow: 0 25px 70px rgba(15,23,42,0.25);
    margin-bottom: 25px;
}
.hero-box h1 {
    font-size: 42px;
    font-weight: 900;
}
.form-panel, .result-panel {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 28px;
    padding: 26px;
    box-shadow: 0 20px 55px rgba(15,23,42,0.08);
}
.insight-card {
    background: rgba(255,255,255,0.88);
    border-radius: 24px;
    padding: 22px;
    border: 1px solid rgba(148,163,184,0.25);
    box-shadow: 0 18px 45px rgba(15,23,42,0.07);
    margin-bottom: 15px;
}
.big-score {
    font-size: 54px;
    font-weight: 900;
    color: #0f172a;
}
.badge {
    display:inline-block;
    padding:8px 14px;
    border-radius:999px;
    background:#e0f2fe;
    color:#0369a1;
    font-weight:900;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <h1>📝 Marks Intelligence Center</h1>
    <p style="font-size:18px;color:#cbd5e1;font-weight:600;">
        Enter subject marks and instantly generate academic score, grade, risk level, strong subjects and weak subject insights.
    </p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([0.9, 1.3])

analysis = None
subjects = None

with left:
    st.markdown('<div class="form-panel">', unsafe_allow_html=True)
    st.subheader("🎯 Enter Student Marks")

    with st.form("marks_form"):
        register_number = st.text_input("Register Number")

        c1, c2 = st.columns(2)
        with c1:
            python = st.number_input("Python", 0, 100, 50)
            dbms = st.number_input("DBMS", 0, 100, 50)
            data_science = st.number_input("Data Science", 0, 100, 50)

        with c2:
            java = st.number_input("Java", 0, 100, 50)
            ai = st.number_input("AI", 0, 100, 50)
            maths = st.number_input("Maths", 0, 100, 50)

        submit = st.form_submit_button("Analyze Performance")

    st.markdown("</div>", unsafe_allow_html=True)

if submit:
    payload = {
        "register_number": register_number,
        "python": python,
        "java": java,
        "dbms": dbms,
        "ai": ai,
        "data_science": data_science,
        "maths": maths
    }

    try:
        res = requests.post(f"{API_URL}/marks/add", json=payload, timeout=5)
        data = res.json()

        if data.get("success"):
            analysis = data["analysis"]
            subjects = {
                "Python": python,
                "Java": java,
                "DBMS": dbms,
                "AI": ai,
                "Data Science": data_science,
                "Maths": maths
            }
        else:
            st.error("Something went wrong while saving marks.")
    except Exception as e:
        st.error(f"Backend error: {e}")

with right:
    if analysis:
        avg = analysis["average"]
        grade = analysis["grade"]
        risk = analysis["risk_level"]

        st.markdown('<div class="result-panel">', unsafe_allow_html=True)
        st.subheader("📊 Performance Result")

        r1, r2, r3 = st.columns(3)
        r1.metric("Total Marks", analysis["total"])
        r2.metric("Average", f"{avg}%")
        r3.metric("Grade", grade)

        st.markdown(f"""
        <div class="insight-card">
            <div class="big-score">{avg}%</div>
            <div class="badge">{risk}</div>
            <p style="color:#64748b;font-weight:700;margin-top:12px;">
                Academic performance score generated from 6 subject marks.
            </p>
        </div>
        """, unsafe_allow_html=True)

        weak = analysis["weak_subjects"]
        strong = analysis["strong_subjects"]

        c1, c2 = st.columns(2)
        with c1:
            st.warning("📚 Weak Subjects: " + (", ".join(weak) if weak else "None"))
        with c2:
            st.success("🔥 Strong Subjects: " + (", ".join(strong) if strong else "None"))

        subject_df = pd.DataFrame({
            "Subject": list(subjects.keys()),
            "Marks": list(subjects.values())
        })

        fig = px.bar(
            subject_df,
            x="Subject",
            y="Marks",
            text="Marks",
            title="Subject-wise Marks"
        )
        fig.update_layout(
            height=330,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=list(subjects.values()),
            theta=list(subjects.keys()),
            fill="toself",
            name="Marks"
        ))
        radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=360,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(radar, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-panel">
            <h3>📈 Waiting for analysis</h3>
            <p style="color:#64748b;font-weight:700;">
                Enter marks and click Analyze Performance to generate instant academic intelligence.
            </p>
            <br>
            <div class="insight-card">
                🎯 Grade Prediction<br>
                ⚠️ Risk Detection<br>
                📚 Weak Subject Detection<br>
                🔥 Strong Subject Detection<br>
                📊 Radar Chart
            </div>
        </div>
        """, unsafe_allow_html=True)