"""
Imports
"""
from db import DBConnector
from replacer import Replacer


class Model:
    """
    Model that contains the current state of the program
    Has a direct connection to the database and the current environment
    """
    def __init__(self):
        self.text = ""
        self.current_env = None
        self.envs = {}
        self.DBConnector = DBConnector()

    def switch_env(self, new_env: str):
        """
        Method to switch to a different environment
        :param new_env:
        """
        assert self.envs[new_env] is not None
        self.current_env = self.envs[new_env]
#         TODO: update in front-end, update replacer

    def update(self, text):
        """

        :param text:
        """
        self.state = self.current_env.process(text)

    def update_text(self, new_text) -> None:
        """
        Update the plaintext that is currently used in the model
        :param new_text: The new plain text
        """
        self.text = new_text
        self.process()

    def replace(self) -> None:
        """
        Method used to run the text trough the replacer
        """
        self.replacer.replace(self.text)

    def process(self) -> None:
        """
        Method used to process the current text in the model in the selected environment
        """
        self.current_env.process(self.text)

    def store_report(self) -> None:
        """
        Store the report in the database
        """
        self.db_connector.create()
