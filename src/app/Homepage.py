import streamlit as st
from scripts.common_pages import page_config
from scripts.node_manager import NodeManager
import os

def create_page():
    st.title("Welcome to the Network Manager App")
    page()

def page():
    st.write(f"### Currently {len(st.session_state['node_manager'])} Nodes!")
    st.write("Google Forum to submit data: https://forms.gle/DwxipGdJrvArv4pT9")
    st.write("Official Community Network Graph: https://blob7.github.io/BE-Friendship-Network/")
    st.write("#### Navigation")
    st.page_link("Homepage.py", label="**Homepage:** landing page for the Network Manager app")
    st.page_link("pages/About.py", label="**About:** Information about the author, purpose, and functionalities of this app")
    st.page_link("pages/Full_Network.py", label="**Full Network:** Displays the current Network Graph")
    st.page_link("pages/Manage_Nodes.py", label="**Manage Nodes:** Option to change the data in the graph and allows for signle node view")
    st.page_link("pages/Survey.py", label="**Survey:** Allows you to take the survey from within the app")

   

if __name__ == "__main__":
    if 'node_manager' not in st.session_state:
        st.session_state['node_manager'] = NodeManager(os.path.abspath(r"src\app\data\connections.json"))
    page_config(icon="🩸", title="Bleeding Edge Community Connections app")
    create_page()