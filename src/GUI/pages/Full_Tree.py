import streamlit as st
from scripts.visualize import create_full_graph, make_graph
from scripts.common_pages import page_config

# Streamlit app title
page_config(icon="🌳", title="Bleeding Edge Community Tree")

st.pyplot(make_graph(create_full_graph()))