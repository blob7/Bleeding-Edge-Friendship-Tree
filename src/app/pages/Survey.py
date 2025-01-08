import streamlit as st
import streamlit.components.v1 as components
from scripts.common_pages import page_config

def create_page():
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSecQzU9o60JTEpZeNaCTexX_nRR4C5FkbCCh45ExzU9tHIs3w/viewform", height=800, scrolling=True)

if __name__ == "__main__":
    page_config(icon="📋", title="Survey")
    create_page()