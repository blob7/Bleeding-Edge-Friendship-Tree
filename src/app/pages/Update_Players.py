import streamlit as st
import streamlit.components.v1 as components
from scripts.common_pages import page_config
from scripts.node_manager import NodeManager
from scripts.visualize import create_neighbor_graph
import os

characters = ["Daemon", "Gizmo", "Nidhoggr", "Maeve", "Cass", "Miko", "Kulev", "Azreal", "Zerocool", "El Bastardo", "Buttercup", "Mekko", "Makutu"]

def add_node_form():
    node_manager: NodeManager = st.session_state['node_manager']
    existing_node_names = node_manager.get_node_ids()
    
    st.title("Add a New Player")

    name = st.text_input("Player Name", max_chars=20, help="Case sensitive xbox name")
    level = st.number_input("Level", min_value=1, step=1, help="Level of the player.", value=None)
    char_main = st.selectbox("Main Character", options=characters, help="Most played character", index=None)
    connections = st.multiselect("Friends", options=existing_node_names, help="Optional") 
    submit_button = st.button(label="Add Player")

    if submit_button:
        if not name:
            st.error("Please enter player name")
        elif node_manager.node_exists(name):
            st.error(f"The name '{name}' is already taken. Please enter a unique name.")
        else:
            attributes = {"level": level, "main_char": char_main, "connections": connections}            
            node_manager.add_node(name, attributes)
            node_manager.save_nodes()
            st.success(f"Player '{name}' added successfully!")


def update_node_form():
    node_manager: NodeManager = st.session_state['node_manager'].clone()
    existing_node_names = node_manager.get_node_ids()

    st.title("Update Player Information")
    node = st.selectbox("Player", options=existing_node_names, index=None, help="Xbox Name")

    if node_manager.node_exists(node):
        main_char = node_manager.get_node_attribute(node, "main_char")
        index = characters.index(main_char) if main_char else None
        
        name = st.text_input("Update Name", max_chars=20, help="Case sensitive xbox gamertag", value=node)
        level = st.number_input("Update Level", min_value=1, step=1, help="Level of the player.", value=node_manager.get_node_attribute(node, "level"))
        main_char = st.selectbox("Update Main Character", options=characters, help="Most played character", index=index)
        node_manager.update_node(node, {"id": name, "level": level, "main_char": main_char})

        if st.toggle("Add Connections"):
            connections_added = st.multiselect("Players", options=[name for name in existing_node_names if name != node], help="Connections to be added")
            updated_connections = node_manager.get_connections(node_id=node) + connections_added
            node_manager.update_node(node, {"connections": updated_connections})
        if st.toggle("Remove Connections"):
            connections_removed = st.multiselect("Players", options=node_manager.get_connections(node_id=node), help="Connections to be removed")
            for connection in connections_removed:
                node_manager.remove_connection(node, connection)
        components.html(create_neighbor_graph(node_manager.data, node), height=800)
        submit =  st.button(label="Update player info")
        if submit:
            node_manager.save_nodes()
            st.session_state['node_manager'] = node_manager
            st.success("Updated Player Information!")
            

def remove_node_form():
    node_manager: NodeManager = st.session_state['node_manager']
    existing_node_names = node_manager.get_node_ids()
    
    st.title("Remove Player")
    node = st.selectbox("Player", options=existing_node_names, index=None, help="Xbox Name")
    st.warning("This will remove all data for the player and any connections with this player")
    confirmation = st.text_input("Please Enter 'Confrim' in order to proceed", placeholder="Confirm")
    if st.button(label="Remove Player"):
        if confirmation == "Confirm":
            node_manager.remove_node(node)
            st.success("Player has been removed")
        else:
            st.toast("Confirmation is required")

if __name__ == "__main__":
    page_config(icon="⚙️", title="Manage Users")
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", ["Add Player", "Update Player Information", "Remove Player"])

    if page == "Add Player":
        add_node_form()
    elif page == "Update Player Information":
        update_node_form()
    elif page == "Remove Player":
        remove_node_form()
