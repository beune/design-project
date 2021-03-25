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

    def __init__(self, initialize_view: Callable[['Model'], None], update_view: Callable[['Model'], None]):
        """
        :param initialize_view: a callback function to initialize the view with initial data
        :param update_view: a callback function to update the view when the model changed
        """
        self.initialize_view = initialize_view
        self.update_view = update_view
        self.environments = {}  # Dictionary for environments {name: endpoint}
        self.environment = None
        self.text = ""
        self.tree = ReportNode("Root")
        self.tree_changes = {}

    def retrieve_initial_data(self):
        """
        Retrieve initial data, i.e. data from 'home' endpoint, from the server
        """
        response = requests.get(ENDPOINT)
        self.environments = response.json()['Data']  # get environments. Form: {name: endpoint}
        self.initialize_view(self)

    def retrieve_tree(self):
        """
        Send the text to the server to retrieve the new tree.
        """
        if len(self.text) > 0 and self.environment:
            data = {"text": self.text}
            path = ENDPOINT + "env/" + self.environments[self.environment] + "/"
            response = requests.get(path, json=data)
            if response.status_code == 200:  # TODO handle different status codes?
                self.tree = jsonpickle.decode(response.json()["Data"])
                self.update_view(self)

    def set_text(self, new_text: str):
        """
        Store the new_text, update the tree and notify the view.
        :param new_text: the new text.
        """
        self.text = new_text
        self.retrieve_tree()

    def set_environment(self, new_environment: str):
        """
        Set the environment to new_environment, update the tree and notify the view.
        :param new_environment: the new environment.
        """
        self.environment = new_environment
        self.retrieve_tree()

    def set_changes_map(self, tree_changes):
        """
        Set the tree changes map with changes from front end
        :param tree_changes: the map containing all changes from front end
        """
        self.tree_changes = tree_changes
