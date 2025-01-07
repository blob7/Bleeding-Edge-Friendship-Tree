import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from app.scripts.node_manager import NodeManager

class TestNodeManager(unittest.TestCase):
    def setUp(self):
        self.node_manager = NodeManager()
        
    def test_clone(self):
        # Set up
        self.node_manager.add_node("Node1", {"attr": "val"})
        cloned_manager = self.node_manager.clone()

        # Test 1: Ensure the clone is not the same object as the original
        self.assertIsNot(cloned_manager, self.node_manager)

        # Test 2: Ensure the cloned data is equal to the original data
        self.assertEqual(cloned_manager.data, self.node_manager.data)

        # Test 3: Ensure the cloned data is a deep copy (modifying one doesn't affect the other)
        cloned_manager.update_node("Node1", {"attr": "modified"})
        self.assertNotEqual(cloned_manager.get_node_attribute("Node1", "attr"), self.node_manager.get_node_attribute("Node1", "attr"))

        # Test 4: Ensure the file_path is copied correctly
        self.assertEqual(cloned_manager.file_path, self.node_manager.file_path)

        # Test 5: Ensure the cloned file_path is not linked (if modified, the original is not affected)
        cloned_manager.file_path = "/new/path"
        self.assertNotEqual(cloned_manager.file_path, self.node_manager.file_path)

    def test_add_node(self):
        # Set up
        self.node_manager.add_node("Node1")

        # Test 1: Adding a node with no attributes (connections should be empty)
        self.assertIn("Node1", self.node_manager.data["nodes"])
        self.assertEqual(self.node_manager.get_node_attribute("Node1", "connections"), [])

        # Test 2: Adding a node with explicit attributes, including connections
        self.node_manager.add_node("Node2", {"connections": ["Node1"]})
        self.assertIn("Node2", self.node_manager.data["nodes"])
        self.assertEqual(self.node_manager.get_node_attribute("Node2", "connections"), ["Node1"])

        # Test 3: Adding a node with attributes but without specifying connections (should default to empty list)
        self.node_manager.add_node("Node3", {"other_attribute": "value"})
        self.assertIn("Node3", self.node_manager.data["nodes"])
        self.assertEqual(self.node_manager.get_node_attribute("Node3", "connections"), [])
        
        with self.assertRaises(ValueError):
            self.node_manager.add_node("Node1")  # Test 4. Node1 already exists, should raise ValueError

    def test_remove_node(self):
        # Set up
        self.node_manager.add_node("Node1", {"connections": ["Node2"]})
        self.node_manager.add_node("Node2", {"connections": ["Node1"]})
        
        # Test 1: Removing a node and checking if it's removed from both the node list and connections
        self.node_manager.remove_node("Node1")
        self.assertNotIn("Node1", self.node_manager.get_node_ids())
        self.assertNotIn("Node1", self.node_manager.get_connections("Node2"))

        # Test 2: Attempting to remove a non-existent node (should raise KeyError)
        with self.assertRaises(KeyError):
            self.node_manager.remove_node("Node3")  # Node3 does not exist, should raise KeyError

    def test_node_exists(self):
        # Test 1: Checking if a non-existent node exists
        self.assertFalse(self.node_manager.node_exists("Node1"))
        
        # Test 2: Checking if a existing node exists
        self.node_manager.add_node("Node1")
        self.assertTrue(self.node_manager.node_exists("Node1"))

    def test_get_node_ids(self):
        self.node_manager.add_node("Node1")
        self.node_manager.add_node("Node2")
        self.assertListEqual(self.node_manager.get_node_ids(), ["Node1", "Node2"])

    def test_get_connections(self):
        # Set up
        self.node_manager.add_node("Node1", {"connections": ["Node2"]})
        
        # Test 1: Verify that the connections for "Node1" return the correct list
        self.assertListEqual(self.node_manager.get_connections("Node1"), ["Node2"])
        
        # Test 2: Verify that an exception (KeyError) is raised when trying to get connections of a non-existent node
        with self.assertRaises(KeyError):
            self.node_manager.get_connections("Node3")

    def test_node_manager_len(self):
        # Test 1: Getting node count with zero nodes
        self.assertEqual(len(self.node_manager), 0)
        
        # Test 2: Getting the node count after adding a node
        self.node_manager.add_node("Node1")
        self.assertEqual(len(self.node_manager), 1)

    def test_remove_connection(self):
        # Set up
        self.node_manager.add_node("Node1", {"connections": ["Node2", "Node3"]})
        self.node_manager.add_node("Node2", {"connections": ["Node1"]})
        self.node_manager.add_node("Node3", {"connections": []})
        
        # Test 1: Successfully remove multiple connections
        self.node_manager.remove_connection("Node1", "Node2")
        self.assertNotIn("Node2", self.node_manager.get_connections("Node1"))
        self.assertIn("Node3", self.node_manager.get_connections("Node1"))

        # Test 2: Try to remove a connection that does not exist, should raise ValueError
        with self.assertRaises(ValueError):
            self.node_manager.remove_connection("Node1", "Node4")

        # Test 3: Try to remove a connection from a non-existing node, should raise KeyError
        with self.assertRaises(KeyError):
            self.node_manager.remove_connection("Node99", "Node2")

    def test_update_node(self):
        # Set up
        self.node_manager.add_node("Node1", {"connections": [], "attr": "value1"})
        self.node_manager.add_node("Node2", {"connections": ["Node1"], "attr": "value2"})

        # Test 1: Update the attributes of "Node1" and verify the change
        self.node_manager.update_node("Node1", {"attr": "new_value"})
        self.assertEqual(self.node_manager.get_node_attribute("Node1", "attr"), "new_value")

        # Test 2: Change the id of "Node1" to "NewId" and verify the change
        self.node_manager.update_node("Node1", {"id": "NewId"})
        self.assertIn("NewId", self.node_manager.data["nodes"])
        self.assertNotIn("Node1", self.node_manager.data["nodes"])
        self.assertIn("NewId", self.node_manager.get_connections("Node2"))
        
        # Test 3: Add an attribute to Node2 (which doesn't exist initially)
        self.node_manager.add_node("Node3")
        self.node_manager.update_node("Node3", {"new_attr": "new_value"})
        self.assertEqual(self.node_manager.get_node_attribute("Node3", "new_attr"), "new_value")

        # Test 4: Try updating a non-existent node and expect a ValueError
        with self.assertRaises(ValueError):
            self.node_manager.update_node("NonExistentNode", {"attr": "value"})

        # Test 5: Try changin the id of an existing node to a id that is already taken, expect a ValueError
        with self.assertRaises(ValueError):
            self.node_manager.update_node("NewId", {"id": "Node2"})


    def test_get_node_attribute(self):
        # Set up
        self.node_manager.add_node("Node1", {"attr": "value"})
        
        # Test 1: Check if we can retrieve the correct attribute value for "Node1"
        self.assertEqual(self.node_manager.get_node_attribute("Node1", "attr"), "value")

        # Test 2: Try retrieving a non-existent attribute for "Node1" and expect a KeyError
        with self.assertRaises(KeyError):
            self.node_manager.get_node_attribute("Node1", "nonexistent")
        
        # Test 3: Try retrieving an attribute from a non-existent node "Node2" and expect a KeyError
        with self.assertRaises(KeyError):
            self.node_manager.get_node_attribute("Node2", "attr")


if __name__ == "__main__":
    unittest.main()