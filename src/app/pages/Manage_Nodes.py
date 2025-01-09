import streamlit as st
import streamlit.components.v1 as components
from scripts.common_pages import page_config
from scripts.node_manager import NodeManager
from scripts.visualize import create_neighbor_graph

characters = ["Daemon", "Gizmo", "Nidhoggr", "Maeve", "Cass", "Miko", "Kulev", "Azreal", "ZeroCool", "El Bastardo", "Buttercup", "Mekko", "Makutu"]

def add_node_form():
    node_manager: NodeManager = st.session_state['node_manager']
    existing_node_names = node_manager.get_node_ids()
    
    st.title("Add a New Player")

    name = st.text_input("Player Name", max_chars=20, help="Case sensitive xbox name")
    level = st.number_input("Level", min_value=1, step=1, help="Level of the player.", value=None)
    char_main = st.selectbox("Main Character", options=characters, help="Most played character", index=None)
    connections = st.multiselect("Friends", options=existing_node_names, help="Optional") 
    survey_completed = st.toggle("Has completed survey / census")
    submit_button = st.button(label="Add Player")

    if submit_button:
        if not name:
            st.error("Please enter player name")
        elif node_manager.node_exists(name):
            st.error(f"The name '{name}' is already taken. Please enter a unique name.")
        else:
            attributes = {"level": level, "main_char": char_main, "connections": connections, "survey_completed": survey_completed}            
            node_manager.add_node(name, attributes)
            node_manager.save_nodes()
            st.success(f"Player '{name}' added successfully!")


def update_node_form():
    node_manager: NodeManager = st.session_state['node_manager']
    cloned_node_manager = node_manager.clone()
    existing_node_names = node_manager.get_node_ids()

    st.title("Update Player Information")
    node = st.selectbox("Player", options=existing_node_names, index=None, help="Xbox Name")

    if node_manager.node_exists(node):
        main_char = node_manager.get_node_attribute(node, "main_char")
        index = characters.index(main_char) if main_char else None
        
        name = st.text_input("Update Name", max_chars=20, help="Case sensitive xbox gamertag", value=node)
        level = st.number_input("Update Level", min_value=1, step=1, help="Level of the player.", value=node_manager.get_node_attribute(node, "level"))
        main_char = st.selectbox("Update Main Character", options=characters, help="Most played character", index=index)
        survey_completed = st.toggle("Has completed survey / census", value=node_manager.get_node_attribute(node, "survey_completed"))
        cloned_node_manager.update_node(node, {"id": name, "level": level, "main_char": main_char, "survey_completed": survey_completed})

        existing_connections = cloned_node_manager.get_connections(name)
        remaining_options = []
        for p_conn in existing_node_names:
            if p_conn != name and p_conn not in existing_connections:
                remaining_options.append(p_conn)
       
        connections_added = st.multiselect("Add Connections", options=remaining_options, help="Connections to be added")
        updated_connections = node_manager.get_connections(node) + connections_added
        cloned_node_manager.update_node(name, {"connections": updated_connections})
        
        connections_removed = st.multiselect("Remove Connections", options=node_manager.get_connections(node), help="Connections to be removed")
        for connection in connections_removed:
            cloned_node_manager.remove_connection(name, connection)
        
        submit =  st.button(label="Save updated player information")
        if submit:
            cloned_node_manager.save_nodes()
            st.session_state['node_manager'] = cloned_node_manager
            st.success("Updated Player Information!")
        components.html(create_neighbor_graph(cloned_node_manager.data, name), height=800)

def remove_node_form():
    node_manager: NodeManager = st.session_state['node_manager']
    existing_node_names = node_manager.get_node_ids()
    
    st.title("Remove Player")
    node = st.selectbox("Player", options=existing_node_names, index=None, help="Xbox Name")
    st.warning("This will remove all data for the player and any connections with this player")
    confirmation = st.text_input("Please Enter 'Confrim' in order to proceed", placeholder="Confirm")
        
    if st.button(label="Remove Player"):
        if not node_manager.node_exists(node):
            st.error("Please enter a valid player name")
            return
        if confirmation == "Confirm":
            node_manager.remove_node(node)
            st.success("Player has been removed")
        else:
            st.toast("Confirmation is required")

if __name__ == "__main__":
    page_config(icon="⚙️", title="Manage Users")
    st.sidebar.title("Navigation")
    
    if 'node_manager' not in st.session_state:
        st.write("Please Return to Homepage to load data")
    else:
        page = st.sidebar.selectbox("Select Page", ["Add Player", "Update Player Information", "Remove Player"])

        if page == "Add Player":
            add_node_form()
        elif page == "Update Player Information":
            update_node_form()
        elif page == "Remove Player":
            remove_node_form()
