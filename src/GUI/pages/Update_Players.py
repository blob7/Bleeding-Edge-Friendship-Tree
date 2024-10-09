import streamlit as st
from scripts.common_pages import page_config
import scripts.nodes as nodes
import scripts.visualize as betree

characters = ["Daemon", "Gizmo", "Nidhoggr", "Maeve", "Cass", "Miko", "Kulev", "Azreal", "Zerocool", "El Bastardo", "Buttercup", "Mekko", "Makutu"]

def add_node_form():
    existing_node_names = nodes.get_node_list()
    
    st.title("Add a New Player")

    name = st.text_input("Player Name", max_chars=20, help="Please use exact case sensitive xbox name")
    level = st.number_input("Level", min_value=1, step=1, help="Level of the player.", value=None)
    char_main = st.selectbox("Main Character", options=characters, help="Most played character", index=None)
    connections = st.multiselect("Friends", options=existing_node_names, help="Optional") 
    submit_button = st.button(label="Add Player")

    if submit_button:
        if not name:
            st.error("Please enter player name")
        elif not nodes.is_unique_node(name=name):
            st.error(f"The name '{name}' is already taken. Please enter a unique name.")
        else:
            attributes = {"level": level, "main_char": char_main, "connections": connections}            
            nodes.add_node(name, attributes)
            st.success(f"Player '{name}' added successfully!")


def update_node_form():
    existing_node_names = nodes.get_node_list()

    st.title("Update Player Information")
    node = st.selectbox("Player", options=existing_node_names, index=None, help="Xbox Name")
    main_char = nodes.get_node_attribute(node, "main_char")
    if main_char is not None:
        index = characters.index(main_char)
    else:
        index = None
    name = st.text_input("Update Name", max_chars=20, help="Case sensitive xbox gamertag", value=node)
    level = st.number_input("Update Level", min_value=1, step=1, help="Level of the player.", value=nodes.get_node_attribute(node, "level"))
    main_char = st.selectbox("Update Main Character", options=characters, help="Most played character", index=index)
    attributes = {"level": level, "main_char": main_char}

    if node:
        display_graph = st.empty()
        current_graph = betree.create_neighbors_graph(node)
        display_graph.pyplot(betree.make_graph(current_graph)) 
        connections_added = None
        connections_removed = None

        if st.toggle("Add Connections"):
            connections_added = st.multiselect("Players", options=[name for name in existing_node_names if name != node], help="Connections to be added")
            current_graph = (betree.create_add_preview_graph(base_node=node, new_nodes=connections_added, G = current_graph))
        if st.toggle("Remove Connections"):
            connections_removed = st.multiselect("Players", options=nodes.get_connections(node_id=node), help="Connections to be removed")
            current_graph = (betree.create_remove_preview_graph(base_node=node, remove_nodes=connections_removed, G= current_graph))
        display_graph.pyplot(betree.make_graph(current_graph)) # Might want to shrink graph 

        submit =  st.button(label="Update player info")
        if submit:
            if connections_added:
                nodes.add_connections(node, connections_added)
            if connections_removed:
                nodes.remove_connections(node, connections_removed)
            if name or attributes:
                nodes.update_node_attributes(node, name, attributes)
            st.success("Updated Player Information!")

def remove_node_form():
    existing_node_names = nodes.get_node_list()
    st.title("Remove Player")
    node = st.selectbox("Player", options=existing_node_names, index=None, help="Xbox Name")
    st.warning("This will remove all data for the player and any connections with this player")
    confirmation = st.text_input("Please Enter 'Confrim' in order to proceed", placeholder="Confirm")
    if st.button(label="Remove Player"):
        if confirmation == "Confirm":
            nodes.remove_node(node)
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
