import os
import json

json_file_path = os.path.abspath("src/Connections.json")

def load_nodes():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            return json.load(f)
    return {"nodes": {}}

def save_node(name, attributes):
    data = load_nodes()
    if "nodes" not in data:
        data["nodes"] = {}
    data["nodes"][name] = attributes
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

        
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

def valid_nodes(): # will return true if connections match or false if issue
    pass