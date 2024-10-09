import streamlit as st
from scripts.common_pages import page_config
from scripts.nodes import get_node_count

def create_page():
    description()
    contact()

def contact():
    st.write("Bleeding Edge Community Tree")
    st.write(f"Currently {get_node_count()} Nodes!")
    st.write("Link to google Forum to submit data")
    st.subheader("Description")
    st.write("This is goofy app")
    st.subheader("Navigation")
    st.write("* About: Shows more information")
    st.write("* ...")

def description():
    st.title("The Bleeding Edge Connections Web")

def main():
    page_config(icon="🩸", title="Bleeding Edge Community Tree app")
    create_page()

if __name__ == "__main__":
    main()