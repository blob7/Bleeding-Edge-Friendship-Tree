from pyvis.network import Network
from data.node_styles import node_styles


def __add_nodes_to_network(net: Network, nodes: dict) -> None:
    """
    Adds nodes to the network graph.
    """
    for node_name, attributes in nodes.items():
        level = attributes.get('level', 'Unknown') if attributes.get('level') is not None else 'Unknown'
        main_char = attributes.get('main_char', 'Unknown') if attributes.get('main_char') is not None else 'Unknown'
        style=node_styles.get(main_char, node_styles.get("Default"))
        
        net.add_node(
            node_name,
            label=node_name,
            title=f"Level: {level} | Main Character: {main_char}",
            image=style.get("image", ""),
            shape='circularImage',
            borderWidth="0",
            borderWidthSelected="5",
            color=style.get("color"),
            shadow=True            
        )

def __add_edges_to_network(net: Network, nodes: dict) -> None:
    """
    Adds edges to the network graph, supporting one-way and bidirectional connections.
    """
    added_edges = set()
    for node_name, attributes in nodes.items():
        for connection in attributes.get("connections", []):
            if connection in nodes:
                if (connection, node_name) in added_edges:
                    net.edges = [
                        edge
                        for edge in net.edges
                        if not ((edge["from"] == connection and edge["to"] == node_name) or
                                (edge["from"] == node_name and edge["to"] == connection))
                    ]
                    net.add_edge(connection, node_name, arrows="to, from", shadow=True)
                else:
                    net.add_edge(node_name, connection, arrows="to", shadow=True)
                added_edges.add((node_name, connection))
                added_edges.add((connection, node_name))
            else:
                print(f"Warning: Connection target '{connection}' for node '{node_name}' does not exist.")


def create_full_graph(data: dict) -> str:
    """
    Creates a graph with all nodes and connections.
    """
    net = Network(bgcolor="#202c40", font_color="white", height = "750px")
    nodes = data.get("nodes", {})
    net.barnes_hut(central_gravity=1, overlap=0.5)
    
    __add_nodes_to_network(net, nodes)
    __add_edges_to_network(net, nodes)
    
    return net.generate_html()

def create_neighbor_graph(data: dict, node_name: str) -> str:
    """
    Creates a graph showing a specific node and its immediate neighbors.
    """
    net = Network()
    nodes = data.get("nodes", {})

    if node_name not in nodes:
        raise ValueError(f"Node '{node_name}' does not exist in the data.")

    # Add the selected node
    __add_nodes_to_network(net, {node_name: nodes[node_name]})
    
    # Add its neighbors and connections
    neighbors = nodes[node_name].get("connections", [])
    neighbor_nodes = {neighbor: nodes[neighbor] for neighbor in neighbors if neighbor in nodes}
    
    __add_nodes_to_network(net, neighbor_nodes)
    for neighbor in neighbors:
        if neighbor in nodes:
            net.add_edge(node_name, neighbor, arrows="to")
            if node_name in nodes[neighbor].get("connections", []):
                net.add_edge(neighbor, node_name, arrows="to, from")

    return net.generate_html()
