import json
import networkx as nx
import matplotlib.pyplot as plt
import os

json_file_path = os.path.abspath("src/Connections.json")

def load_data():
    with open(json_file_path, 'r') as f:
        return json.load(f)

def create_full_graph():
    data = load_data()
    G = nx.Graph()
    for node_id, attributes in data["nodes"].items():
        G.add_node(node_id, level=attributes["level"])
        for connection in attributes["connections"]:
            G.add_edge(node_id, connection, color="black")
    return G.copy()

def make_graph(G):
    pos = nx.spring_layout(G, k=0.6, seed=42)
    levels = nx.get_node_attributes(G, 'level')
    default_color = 1
    node_colors = [levels.get(node, default_color) for node in G.nodes()]

    
    plt.figure(figsize=(12, 8), facecolor='#FFF9DB')  # Doesnt work for some reason
    nx.draw(
        G, pos, with_labels=True, node_size=1750,
        node_color=node_colors, cmap=plt.cm.Oranges,
        font_size=6, font_color="black", font_weight="bold",
        edge_color=[G[u][v]['color'] if 'color' in G[u][v] else 'black' for u, v in G.edges()], 
        width=1
    )
    return plt

def create_add_preview_graph(base_node, new_nodes, G):
    G = G if G else create_full_graph()
    for node in new_nodes:
        G.add_node(node)
        G.add_edge(base_node, node, color='green', width = 1)
    return G.copy()

def create_remove_preview_graph(base_node, remove_nodes, G):
    G = G if G else create_full_graph()
    for node in remove_nodes:
        if G.has_edge(base_node, node):
            G[base_node][node]['color'] = 'red'
    return G.copy()
    
def create_neighbors_graph(node, G = None):
    G = G if G else create_full_graph()
    immediate_nodes = [node] + list(G.neighbors(node))
    return G.subgraph(immediate_nodes).copy()
     