"""
Imports
"""
from Model import Model
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
