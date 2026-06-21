import streamlit as st
from navbar import show_navbar

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
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

if "theme" not in st.session_state:
    st.session_state.theme = "Ocean Blue"

st.title("⚙️ Theme Settings")

theme = st.selectbox(
    "Choose Theme",
    [
        "Ocean Blue",
        "Academic Purple",
        "Emerald Green",
        "Dark Mode"
    ],
    index=[
        "Ocean Blue",
        "Academic Purple",
        "Emerald Green",
        "Dark Mode"
    ].index(st.session_state.theme)
)

if st.button("Apply Theme"):
    st.session_state.theme = theme
    st.success(f"{theme} Applied")
