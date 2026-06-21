import streamlit as st

def apply_theme():

    if "theme" not in st.session_state:
        st.session_state.theme = "Ocean Blue"

    themes = {

        "Ocean Blue": {
            "bg": "linear-gradient(135deg,#f8fafc,#dbeafe,#ecfeff)",
            "card": "#ffffff",
            "text": "#0f172a",
            "accent": "#2563eb"
        },

        "Academic Purple": {
            "bg": "linear-gradient(135deg,#faf5ff,#ede9fe,#f5f3ff)",
            "card": "#ffffff",
            "text": "#2e1065",
            "accent": "#7c3aed"
        },

        "Emerald Green": {
            "bg": "linear-gradient(135deg,#ecfdf5,#d1fae5,#f0fdf4)",
            "card": "#ffffff",
            "text": "#064e3b",
            "accent": "#059669"
        },

        "Dark Mode": {
            "bg": "linear-gradient(135deg,#020617,#0f172a,#111827)",
            "card": "#1e293b",
            "text": "#f8fafc",
            "accent": "#38bdf8"
        }
    }

    t = themes[st.session_state.theme]

    st.markdown(
        f"""
        <style>

        .stApp {{
            background: {t["bg"]};
            color: {t["text"]};
        }}

        .theme-card {{
            background: {t["card"]};
            color: {t["text"]};
            border-radius: 24px;
            padding: 25px;
            border: 1px solid rgba(148,163,184,0.2);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )