"""
Imports
"""
from typing import Callable

import jsonpickle
import requests

from src.report_node import ReportNode

ENDPOINT = "http://127.0.0.1:5000/"


class Model:
    """
    Model contains the state of the client application.
    """
    def __init__(self, notify: Callable[['Model'], None]):
        self.environment = "mammo"
        self.text = ""
        self.tree = ReportNode("Root")
        self.notify_view = notify

    def retrieve_tree(self):
        """
        Send the text to the server to retrieve the new tree.
        """
        data = {"text": self.text}
        response = requests.get(ENDPOINT + self.environment, json=data)
        self.tree = jsonpickle.decode(response.json()["Data"])

    def set_text(self, new_text: str):
        """
        Store the new_text, update the tree and notify the view.
        :param new_text: the new text.
        """
        self.text = new_text
        self.retrieve_tree()
        self.notify_view(self)

    def set_environment(self, new_environment: str):
        """
        Set the environment to new_environment, update the tree and notify the view.
        :param new_environment: the new environment.
        """
        self.environment = new_environment
        self.retrieve_tree()
        self.notify_view(self)
