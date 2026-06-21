import streamlit as st

from navbar import show_navbar

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")
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
st.switch_page("app.py")