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
        self.environment = []
        self.envs = {}
        self.DBConnector = DBConnector()

    def switch_env(self, new_env):
        """
        Method to switch to a different environment
        :param new_env:
        """
        if self.envs[new_env] is not None:
            self.environment = self.envs[new_env]
        else:
            pass
            # TODO THROW ERROR
