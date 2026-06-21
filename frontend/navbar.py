import streamlit as st

def show_navbar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .block-container {
        padding-top: 2.8rem !important;
    }

    .stButton button {
        background: rgba(15,23,42,0.92) !important;
        color: white !important;
        border-radius: 999px !important;
        border: none !important;
        font-weight: 900 !important;
        padding: 0.65rem 0.7rem !important;
        font-size: 13px !important;
        margin-bottom: 0.35rem !important;
    }

    .stButton button:hover {
        background: linear-gradient(135deg,#06b6d4,#22c55e) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    row1 = st.columns(7)
    pages1 = [
        ("🏠 Dashboard", "app.py"),
        ("🎓 Students", "pages/students.py"),
        ("📝 Marks", "pages/marks.py"),
        ("📊 Analytics", "pages/analytics.py"),
        ("🤖 AI", "pages/ai_insights.py"),
        ("🏆 Board", "pages/leaderboard.py"),
        ("👤 Profile", "pages/profile.py"),
    ]

    for col, (label, path) in zip(row1, pages1):
        with col:
            if st.button(label, use_container_width=True):
                st.switch_page(path)

    row2 = st.columns(6)
    pages2 = [
        ("📈 Trends", "pages/trends.py"),
        ("📄 Reports", "pages/reports.py"),
        ("🧾 PDF", "pages/pdf_reports.py"),
        ("🔔 Alerts", "pages/notifications.py"),
        ("👨‍💼 Admin", "pages/admin.py"),
        ("⚙️ Settings", "pages/settings.py"),
    ]

    for col, (label, path) in zip(row2, pages2):
        with col:
            if st.button(label, use_container_width=True):
                st.switch_page(path)

    st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    st.divider()
