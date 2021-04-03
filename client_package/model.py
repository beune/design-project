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
        self.tree = Node("Root")
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
        if isinstance(node, LabelNode):
            change = self.back_changes.get(self.tree_identifiers[id(node)])
            if change:
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
        if self.environment:
            self.view.show_loader(True)
            self.text = new_text
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

    #     TODO: CREATE JSONREPRESENTATION OF THE TREE WITH CHANGES
    def add_to_db(self):
        """
        Method used to store the current tree into the database
        """
        data = {"jsonrep": "Teststring"}
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

    def set_back_change(self, identifier: str, new_label: str):
        """
        Method used to set changes relevant for the state of the tree
        :param identifier: identifier of the changed node
        :param new_label: The new label for the changed node
        """
        self.back_changes[identifier] = BackChange(new_label)

    def set_front_change(self, identifier, warning: bool):
        """
        Method used to set changes irrelevant for the state of the tree
        :param identifier: identifier of the changed node
        :param warning: Whether the warning for the node needs to be on or off
        """
        self.front_changes[identifier] = FrontChange(warning)
