import streamlit as st
import streamlit.components.v1 as components
from scripts.visualize import create_full_graph
from scripts.common_pages import page_config

def create_page():
    graph_html = create_full_graph(st.session_state["node_manager"].data)
    components.html(graph_html, height=800)

if __name__ == "__main__":
    if 'node_manager' not in st.session_state:
        st.write("Please Return to Homepage to load data")
    else:
        page_config(icon="🕸️", title="Bleeding Edge Community Network")
        create_page()