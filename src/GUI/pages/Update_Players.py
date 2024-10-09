import streamlit as st
from scripts.common_pages import page_config
import scripts.nodes as nodes
import scripts.visualize as betree


# Streamlit form for adding a node
def add_node_form():
    existing_node_names = nodes.get_node_list()
    characters = ["Daemon", "Gizmo", "Nidhoggr", "Maeve", "Cass", "Miko", "Kulev", "Azreal", "Zerocool", "El Bastardo", "Buttercup", "Mekko", "Makutu"]
    
    st.title("Add a New Player")

    name = st.text_input("Player Name", max_chars=20, help="Please use exact case sensitive xbox name")
    level = st.number_input("Level", min_value=10, step=1, help="Level of the player. 10+ required")
    char_main = st.selectbox("Main Character", options=characters, help="Most played character")
    connections = st.multiselect("Friends", options=existing_node_names, help="Optional") 
    submit_button = st.button(label="Add Player")

    if submit_button:
        if not (name or level):
            st.error("Please enter player name and level")
        elif not nodes.is_unique_node(name=name):
            st.error(f"The name '{name}' is already taken. Please enter a unique name.")
        else:
            attributes = {"level": level, "main_char": char_main, "connections": connections}            
            nodes.save_node(name, attributes)
            st.success(f"Player '{name}' added successfully!")


# Streamlit form for changing connections
def update_node_form():
    existing_node_names = nodes.get_node_list()

    st.title("Update Player Information")

    # Select nodes to connect/disconnect
    node = st.selectbox("Player 1", options=existing_node_names, index=None)
    if node:
     
        display_graph = st.empty()
        current_graph = betree.create_neighbors_graph(node)
        display_graph.pyplot(betree.make_graph(current_graph)) 
        
        

        if st.toggle("Add Connections"):
            connections_added = st.multiselect("Players", options=[name for name in existing_node_names if name != node], help="Connections to be added")
            current_graph = (betree.create_add_preview_graph(base_node=node, new_nodes=connections_added, G = current_graph))
        if st.toggle("Remove Connections"):
            connections_removed = st.multiselect("Players", options=nodes.get_connections(node_id=node), help="Connections to be removed")
            display_graph.pyplot(betree.make_graph(betree.create_remove_preview_graph(base_node=node, remove_nodes=connections_removed)))

        # Submit button
        submit_connection = st.button(label="Update Connection")

        # Handle form submission
        if submit_connection:
            # Find nodes in data
            st.success("wee")
            # node1_data = next((node for node in data["nodes"] if node["id"] == node1), None)
            # node2_data = next((node for node in data["nodes"] if node["id"] == node2), None)

            # if not node1_data or not node2_data:
            #     st.error("One or both nodes not found.")
            #     return

            # # Update connections based on action
            # if action == "Add Connection":
            #     if node2 not in node1_data["connections"]:
            #         node1_data["connections"].append(node2)
            #     if node1 not in node2_data["connections"]:
            #         node2_data["connections"].append(node1)
            #     st.success(f"Connection added between {node1} and {node2}.")
            
            # elif action == "Remove Connection":
            #     if node2 in node1_data["connections"]:
            #         node1_data["connections"].remove(node2)
            #     if node1 in node2_data["connections"]:
            #         node2_data["connections"].remove(node1)
            #     st.success(f"Connection removed between {node1} and {node2}.")

            # # Save updated data to JSON file
            # nodes.save_nodes(data)

# Run the app
if __name__ == "__main__":
    page_config(icon="⚙️", title="Manage Users")
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", ["Add Player", "Update Player Information", "Remove Player"])

    if page == "Add Player":
        add_node_form()
    elif page == "Update Player Information":
        update_node_form()
    elif page == "Remove Player":
        pass
