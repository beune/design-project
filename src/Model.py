"""
Imports
"""
from DBConnector import DBConnector


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
#         TODO: update in front-end

    def update_text(self, new_text):
        self.text = new_text
