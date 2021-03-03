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
