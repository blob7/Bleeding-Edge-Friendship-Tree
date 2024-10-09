import streamlit as st
from scripts.common_pages import page_config

def create_page():
    description()
    contact()

def contact():
    st.write("Author: Blob")
    st.write("Contact: Discord: blobfishpro")

def description():
    st.title("Description")

def main():
    page_config(icon="🌐", title="About")
    create_page()

if __name__ == "__main__":
    main()