"""
Imports
"""
import asyncio
from typing import Callable

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

    async def retrieve_tree(self):
        """
        Asynchronous call for retrieving a new tree and notifying the view.
        """
        import pickle
        with open("TESTPICKLE.pkl", "rb") as file:
            self.tree = pickle.load(file)
        # data = {"text": self.text}
        # response = requests.get(ENDPOINT + self.environment, json=data)
        # self.tree = jsonpickle.decode(response.json()["Data"])
        self.notify_view(self)

    def set_text(self, new_text: str):
        """
        Store the new_text, update the tree and notify the view.
        :param new_text: the new text.
        """
        self.text = new_text
        asyncio.run(self.retrieve_tree())

    def set_environment(self, new_environment: str):
        """
        Set the environment to new_environment, update the tree and notify the view.
        :param new_environment: the new environment.
        """
        self.environment = new_environment
        asyncio.run(self.retrieve_tree())
