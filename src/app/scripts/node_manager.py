import os
import json
import copy

class NodeManager:  
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path
        if file_path:
            self.data = self._load_nodes()
        else:
            self.data = {"nodes": {}}
            
    def __len__(self):
        return len(self.data["nodes"])

    def _load_nodes(self) -> dict:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def clone(self) -> "NodeManager":
        cloned_instance = NodeManager()
        cloned_instance.data = copy.deepcopy(self.data)
        cloned_instance.file_path = self.file_path
        return cloned_instance


    def save_nodes(self, file_path: str | None = None) -> None:
        target_path = file_path or self.file_path
        if not target_path:
            raise ValueError("File path is not set. Please pass in a valid file path.")
        with open(target_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_node(self, node_id: str, attributes: dict | None = None) -> None:
        if self.node_exists(node_id):
            raise ValueError(f"Node '{node_id}' already exists.")
        if attributes is None:
            attributes = {"connections": []}
        else:
            attributes.setdefault("connections", [])
        self.data["nodes"][node_id] = attributes

    def remove_node(self, node_id: str) -> None:
        if not self.node_exists(node_id):
            raise KeyError(f"Node '{node_id}' not found.")
        
        for _, attributes in self.data["nodes"].items():
            if node_id in attributes.get("connections", []):
                attributes["connections"].remove(node_id)
        
        del self.data["nodes"][node_id]


    def node_exists(self, node_id: str) -> bool:
        return node_id in self.data["nodes"]

    def get_node_ids(self) -> list:
        return list(self.data["nodes"].keys())

    def get_connections(self, node_id: str) -> list:
        if not self.node_exists:
            raise KeyError(f"Node '{node_id}' not found.")
        return self.data["nodes"][node_id].get("connections", [])


    def remove_connection(self, base_node_id: str, connected_node_id: str) -> None:
        if not self.node_exists(base_node_id):
            raise KeyError(f"Base node '{base_node_id}' not found.")
        connections = self.data["nodes"][base_node_id].get("connections", [])
        if connected_node_id not in connections:
            raise ValueError(f"Connected node '{connected_node_id}' not found in base node '{base_node_id}' connections.")        
        connections.remove(connected_node_id)

    def update_node(self, node_id: str, new_values: dict) -> None:
        if not self.node_exists(node_id):
            raise ValueError(f"Node '{node_id}' does not exist.")
        if not new_values:
            return

        new_id = new_values.get("id")
        if new_id and new_id != node_id:
            if self.node_exists(new_id):
                raise ValueError(f"Node '{new_id}' already exists.")
            
            # Update connections in other nodes
            for _, node_attributes in self.data["nodes"].items():
                if node_id in node_attributes.get("connections", []):
                    node_attributes["connections"].remove(node_id)
                    node_attributes["connections"].append(new_id)
            
            # Rename the node
            self.data["nodes"][new_id] = self.data["nodes"].pop(node_id)
            node_id = new_id  # Update the reference

        # Update other attributes
        for key, value in new_values.items():
            if key == "id":
                continue
            self.data["nodes"][node_id][key] = value


    def get_node_attribute(self, node_id: str, key: str):
        if not self.node_exists(node_id):
            raise KeyError(f"Node '{node_id}' not found.")
        if key not in self.data["nodes"][node_id]:
            raise KeyError(f"Key '{key}' not found in node '{node_id}'")
        return self.data["nodes"][node_id][key]
            
        