import streamlit as st
from scripts.common_pages import page_config

def create_page():
    st.title("About")
    description()
    contact()

def contact():
    st.subheader("Contact")
    st.write(r"* Discord: <a href='https://discordapp.com/users/437323522352873472'>blobfishpro</a>", unsafe_allow_html=True)
    st.write(r"* Github: <a href='https://github.com/blob7'>blob7</a>", unsafe_allow_html=True)
    st.write("* Xbox: @BlobFishPro")

def description():
    st.write("Author: Blob")
    st.write(
        """The Bleeding Edge Community Network project was created as a fun way to demonstrate the interconnectivity
        of the community. Bleeding Edge has historically had a tight-knit community where word of mouth spreads quickly.
        It has also witnessed the formation of 'factions' and the drama between them. This project aims to showcase the
        complex ways in which our community is connected. Data is collected by surveying community members, and
        connections are at the discretion of the individuals involved, meaning some relationships can be one-way. If any
        data seems incorrect or needs updating, please let me know."""
        )
 
if __name__ == "__main__":
    page_config(icon="🌐", title="About")
    create_page()