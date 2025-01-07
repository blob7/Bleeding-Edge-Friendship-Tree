import streamlit as st
from scripts.common_pages import page_config
from scripts.node_manager import NodeManager
import os

def create_page():
    description()
    contact()

def contact():
    st.write("Bleeding Edge Community Tree")
    st.write(f"Currently {len(st.session_state['node_manager'])} Nodes!")
    st.write("Link to google Forum to submit data: https://forms.gle/DwxipGdJrvArv4pT9")
    st.subheader("Description")
    st.write("...")
    st.subheader("Navigation")
    st.write("* About: Shows more information")
    st.write("* ...")

def description():
    st.title("The Bleeding Edge Connections Web")

def main():
    page_config(icon="🩸", title="Bleeding Edge Community Tree app")
    create_page()

if __name__ == "__main__":
    if 'node_manager' not in st.session_state:
        st.session_state['node_manager'] = NodeManager(os.path.abspath("src\data\connections.json"))
    main()