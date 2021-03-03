from Backend.Model import Model
from Backend.NPUIAutomation import NPUIAutomation
from Backend.View import View
from threading import Thread
import time


class Controller:

    def __init__(self):
        self.model = Model()
        self.view = View()
        self.UIAutomation = NPUIAutomation()
        self.UIAutomation.start()
