import streamlit as st

def page_config(icon: str, title: str, initilazations: callable = None):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide"
    )
    if initilazations:
        initilazations()
