import streamlit as st
import streamlit.components.v1 as components
from scripts.visualize import create_full_graph
from scripts.common_pages import page_config

page_config(icon="🌳", title="Bleeding Edge Community Network")

graph_html = create_full_graph(st.session_state["node_manager"].data)

components.html(graph_html, height=800)