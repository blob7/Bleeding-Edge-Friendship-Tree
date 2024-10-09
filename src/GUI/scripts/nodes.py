import os
import json

json_file_path = os.path.abspath("src/Connections.json")

def load_nodes():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            return json.load(f)
    return {"nodes": {}}

def save_nodes(data):
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def add_node(name, attributes):
    data = load_nodes()
    connections = attributes["connections"] #adds two way connections through method and inits to none
    attributes["connections"] = []
    data["nodes"][name] = attributes
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    add_connections(name, connections)


def remove_node(name):
    data = load_nodes()
    if name in data["nodes"]:
        for _, attributes in data["nodes"].items():
            if name in attributes.get("connections", []):
                attributes["connections"].remove(name)
        del data["nodes"][name]
        save_nodes(data)
        
def is_unique_node(name):
    data = load_nodes()
    return name not in data["nodes"]

def get_node_list():
    data = load_nodes()
    return list(data["nodes"].keys())

def get_connections(node_id):
    data = load_nodes()
    if node_id in data["nodes"]:
        return data["nodes"][node_id]["connections"]
    else:
        return f"Node '{node_id}' not found."

def get_node_count():
    data = load_nodes()
    return len(data["nodes"]) 

def validate_nodes(): # will return true if connections match or false if issue
    pass

def remove_connections(base_node, connected_nodes):
    data = load_nodes()
    for node in connected_nodes:
        data["nodes"][base_node]["connections"].remove(node)
        data["nodes"][node]["connections"].remove(base_node)
    save_nodes(data)

def add_connections(base_node, connecting_nodes):
    data = load_nodes()
    for node in connecting_nodes:
        data["nodes"][base_node]["connections"].append(node)
        data["nodes"][node]["connections"].append(base_node)
    save_nodes(data)

def update_node_attributes(old_name, new_name=None, attributes=None):
    data = load_nodes()
    if new_name and is_unique_node(new_name):
        for _, node_attributes in data["nodes"].items():
            if old_name in node_attributes["connections"]:
                node_attributes["connections"].remove(old_name)
                node_attributes["connections"].append(new_name)
        node_data = data["nodes"][old_name]
        data["nodes"][new_name] = node_data
        del data["nodes"][old_name]
        old_name = new_name # refrence for attributes
    if attributes:
        for key, value in attributes.items():
            data["nodes"][old_name][key] = value
    save_nodes(data)
    
def get_node_attribute(name, key):
    data = load_nodes()
    if name in data["nodes"]:
        if key in data["nodes"][name]:
            return data["nodes"][name][key]
        else:
            return None