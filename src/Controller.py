"""
Imports
"""
from src.model.model import Model
from UIAutomation import NPUIAutomation
from View import View


class Controller:
    """
    Controller class which controls both the Model and the View
    """
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.UIAutomation = NPUIAutomation()
        self.UIAutomation.start()

    def update_model_text(self) -> None:
        """
        Method used to update the text in the model based on new text in the G2 speech window
        """
        self.model.update_text(self.UIAutomation.get_text())

    def set_replacement(self, key: str, replacement: str):
        """
        Method used to add a new replacement for this environment
        :param key: The new key which should always be replaced
        :param replacement: The new string for which the key should be replaced
        """
        self.model.add_replacement(key, replacement)

    def remove_replacement(self, key: str):
        """
        Method used to remove a replacement in the current environment
        :param key: The key of the replacement which needs to be removed
        """
        self.model.remove_replacement(key)
