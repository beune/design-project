"""
Imports
"""

import jsonpickle
import requests
from reporttree.node import Node
from reporttree.label_node import LabelNode

# ENDPOINT = "https://docker.beune.dev/"
from client_package.tree_changes import BackChange, FrontChange

ENDPOINT = "http://127.0.0.1:5000/"
FRONT = ["warning"]
BACK = ["label", "text"]


class Model:
    """
    Model contains the state of the client application.
    """

    def __init__(self, viewrep):
        """
        Initializes the model
        """
        self.view = viewrep
        self.environments = {}  # Dictionary for environments {name: endpoint}
        self.environment = None
        self.text = ""
        self.colours = {}
        self.tree = Node("report")
        self.tree_identifiers = {}
        self.back_changes = {}
        self.front_changes = {}

    def apply_back_changes(self):
        """
        Method used to apply changes relevant for the state of the reportstructure
        """

        def traverse(node: Node):
            """

            :param node:
            :return:
            """
            for child in node:
                traverse(child)
            self.apply_change(node)

        traverse(self.tree)

    def apply_change(self, node: Node):
        """
        Method used to apply a BackChange
        :param node: The node which needs to be changed
        """
        change = self.back_changes.get(self.tree_identifiers[id(node)], BackChange())
        node.corr_text = change.text
        if isinstance(node, LabelNode):
            node.corr_label = change.label

    def retrieve_initial_data(self):
        """
        Retrieve initial data, i.e. data from 'home' endpoint, from the server
        """
        response = self.get_request(ENDPOINT)
        if response:
            self.environments = response.json()['Data']  # get environments. Form: {name: endpoint}
            self.view.initialize(self)

    def retrieve_tree(self):
        """
        Send the text to the server to retrieve the new tree.
        """
        data = {"text": self.text}
        path = ENDPOINT + "env/" + self.environments[self.environment] + "/"
        response = self.get_request(path, data)
        if response:
            self.tree = jsonpickle.decode(response.json()["Data"])
            self.tree_identifiers = {}
            self.create_identifiers(self.tree)

    def retrieve_colours(self):
        """
        Method used to retrieve the coloring scheme for the environment
        """
        if self.environment:
            path = ENDPOINT + "env/" + self.environments[self.environment] + "/colours"
            response = self.get_request(path)
            if response:
                self.colours = jsonpickle.decode(response.json()["Data"])

    def set_text(self, new_text: str):
        """
        Store the new_text, update the tree and notify the view.
        :param new_text: the new text.
        """
        self.text = new_text
        if self.environment:
            self.view.show_loader(True)
            self.retrieve_tree()
            self.apply_back_changes()
            self.view.update(self)
            self.view.show_loader(False)

    def set_environment(self, new_environment: str):
        """
        Set the environment to new_environment, update the tree and notify the view.
        :param new_environment: the new environment.
        """
        self.view.show_loader(True)
        self.front_changes = {}
        self.back_changes = {}
        self.environment = new_environment
        self.retrieve_colours()
        self.retrieve_tree()
        self.view.update(self)
        self.view.show_loader(False)

    def set_changes_map(self, tree_changes):
        """
        Set the tree changes map with changes from front end
        :param tree_changes: the map containing all changes from front end
        """
        self.tree_changes = tree_changes

    def get_request(self, path: str, data=None):
        """
        Method used to create get requests
        :param path: The path of the get request
        :param data: The data of the get request
        """
        try:
            response = requests.get(path, json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as c:
            self.view.server_error(c.args[0].args[0])
        except requests.exceptions.RequestException as e:
            self.view.server_error(e.args[0])

    def add_to_db(self):
        """
        Method used to store the current tree into the database
        """
        jsonrep = jsonpickle.encode(self.tree)
        data = {"jsonrep": jsonrep}
        try:
            response = requests.post(ENDPOINT + "env/" + self.environments[self.environment] + "/db", json=data)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as c:
            self.view.server_error(c.args[0].args[0])
        except requests.exceptions.RequestException as e:
            self.view.server_error(e.args[0])

    def create_identifiers(self, node):
        """
        Recursively iterates through the given tree, creating identifiers
        :param node The root of the tree
        """
        identifier = node.category
        if identifier not in self.tree_identifiers.values():
            self.tree_identifiers[id(node)] = identifier
        else:
            distinguisher = 1
            while identifier + str(distinguisher) in self.tree_identifiers.values():
                distinguisher += 1
            self.tree_identifiers[id(node)] = identifier + str(distinguisher)

        if not node.is_leaf():
            for child in node.children:
                self.create_identifiers(child)

    def change(self, identifier, changed_type: str, value):
        """
        Method used to set a change
        :param identifier: Identifier of the changed node
        :param changed_type: Type of the change
        :param value: Value of the change
        """
        node_identifier = identifier.replace("_value", "")
        if changed_type in BACK:
            self.set_back_change(node_identifier, changed_type, value)
            self.apply_back_changes()
        elif changed_type in FRONT:
            self.set_front_change(identifier, changed_type, value)

    def set_back_change(self, identifier: str, changed_type: str, value):
        """
        Method used to set changes relevant for the state of the tree
        :param identifier: identifier of the changed node
        :param changed_type: the type of change
        :param value: the new value
        """
        change = self.back_changes.setdefault(identifier, BackChange())
        if hasattr(change, changed_type):
            setattr(change, changed_type, value)

    def set_front_change(self, identifier, changed_type: str, value):
        """
        Method used to set changes irrelevant for the state of the tree
        :param identifier: identifier of the changed node
        :param changed_type: the type of change
        :param value: the value of the change
        """
        change = self.front_changes.setdefault(identifier, FrontChange())
        if hasattr(change, changed_type):
            setattr(change, changed_type, value)

    def reset_node(self, identifier: str):
        """
        Reset all changes for a node
        :param identifier: identifier of either the node or leaf
        """
        node_identifier = identifier.replace("_value", "")
        if node_identifier in self.back_changes:
            self.back_changes.pop(node_identifier)
            self.apply_back_changes()
        if identifier in self.front_changes:
            self.front_changes.pop(identifier)
