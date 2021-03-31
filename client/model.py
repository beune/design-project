"""
Imports
"""
from typing import Callable

import jsonpickle
import requests
from report_tree.report_node import ReportNode

# ENDPOINT = "https://docker.beune.dev/"
ENDPOINT = "http://127.0.0.1:5000/"


class Model:
    """
    Model contains the state of the client application.
    """

    def __init__(self, initialize_view: Callable[['Model'], None], update_view: Callable[['Model'], None],
                 server_error: Callable[[str], None], show_loader: Callable[[bool], None]):
        """
        :param initialize_view: a callback function to initialize the view with initial data
        :param update_view: a callback function to update the view when the model changed
        """
        self.initialize_view = initialize_view
        self.update_view = update_view
        self.server_error = server_error
        self.show_loader = show_loader
        self.environments = {}  # Dictionary for environments {name: endpoint}
        self.environment = None
        self.text = ""
        self.colours = {}
        self.tree = ReportNode("Root")
        self.tree_changes = {}

    def retrieve_initial_data(self):
        """
        Retrieve initial data, i.e. data from 'home' endpoint, from the server
        """
        response = self.get_request(ENDPOINT)
        if response:
            self.environments = response.json()['Data']  # get environments. Form: {name: endpoint}
            self.initialize_view(self)

    def retrieve_tree(self):
        """
        Send the text to the server to retrieve the new tree.
        """
        if len(self.text) > 0 and self.environment:
            data = {"text": self.text}
            path = ENDPOINT + "env/" + self.environments[self.environment] + "/"
            response = self.get_request(path, data)
            if response:
                self.tree = jsonpickle.decode(response.json()["Data"])
                self.update_view(self)

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
        self.show_loader(True)
        self.text = new_text
        self.retrieve_tree()
        self.show_loader(False)

    def set_environment(self, new_environment: str):
        """
        Set the environment to new_environment, update the tree and notify the view.
        :param new_environment: the new environment.
        """
        self.show_loader(True)
        self.environment = new_environment
        self.retrieve_colours()
        self.retrieve_tree()
        self.show_loader(False)

    def set_changes_map(self, tree_changes):
        """
        Set the tree changes map with changes from front end
        :param tree_changes: the map containing all changes from front end
        """
        self.tree_changes = tree_changes

    #     TODO: CREATE JSONREPRESENTATION OF THE TREE WITH CHANGES
    def add_to_db(self):
        """
        Method used to store the current tree into the database
        """
        data = {"jsonrep": "Teststring"}
        try:
            response = requests.post(ENDPOINT, json=data)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as c:
            self.server_error(c.args[0].args[0])
        except requests.exceptions.RequestException as e:
            self.server_error(e.args[0])

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
            self.server_error(c.args[0].args[0])
        except requests.exceptions.RequestException as e:
            self.server_error(e.args[0])
