from pyvis.network import Network

def __add_nodes_to_network(net: Network, nodes: dict) -> None:
    """
    Adds nodes to the network graph.
    """
    for node_name, attributes in nodes.items():
        level = attributes.get('level', 'N/A')  # Default to 'N/A' if level is missing or None
        main_char = attributes.get('main_char', 'Unknown')  # Default to 'Unknown' if main_char is missing or None
        
        net.add_node(
            node_name,
            label=node_name,
            title=f"Level: {level} | Main Character: {main_char}"
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
                    net.add_edge(connection, node_name, arrows="to, from")
                else:
                    net.add_edge(node_name, connection, arrows="to")
                added_edges.add((node_name, connection))
                added_edges.add((connection, node_name))
            else:
                print(f"Warning: Connection target '{connection}' for node '{node_name}' does not exist.")

def create_full_graph(data: dict) -> str:
    """
    Creates a graph with all nodes and connections.
    """
    net = Network()
    nodes = data.get("nodes", {})
    
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
