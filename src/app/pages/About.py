import streamlit as st
from scripts.common_pages import page_config

def create_page():
    st.title("About")
    display_description()
    display_features()
    display_contact()
    
def display_features():
    st.subheader("Features")
    st.write(
        """
        1. **Full Network View**
            * View the the current network graph
        2. **Survey**
            * Take the survey to add your data to the official network graph
        3. **Add player node**
            * Adds a player node to the graph
        4. **Remove player node**
            * Removes a player node from the graph. Deletes all other nodes connection to this node as well
        5. **Update player node**
            * Updates any of the following information about a node (*name, level, main character, connections, survey completion status*)
        6. **View Neighbor Network**
            * Inside of update players, a nodes individual network graph is displayed. *does not include inward connections* 
        """
        )


def display_contact():
    st.subheader("Contact")
    st.write(r"* Discord: <a href='https://discordapp.com/users/437323522352873472'>blobfishpro</a>", unsafe_allow_html=True)
    st.write(r"* Github: <a href='https://github.com/blob7'>blob7</a>", unsafe_allow_html=True)
    st.write("* Xbox: @BlobFishPro")

def display_description():
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