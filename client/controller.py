"""
Imports
"""
import pickle
import jsonpickle
import requests

from client.ui_automation import UIAutomation
from src.report_node import ReportNode


class Controller:
    """
    Client controller of the mcv pattern, directs traffic between view and model
    Also has connection to the server and the UIAutomation
    """

    def __init__(self, ui_automation: UIAutomation = None):
        self.ui_automation = ui_automation
        # self.ui_automation.start()

        # TODO Add model and view, start UIAutomation

    def get_text(self) -> str:
        """
        Method used to get the text from the UIAutomation
        :return: The text of the UIAutomation
        """
        return self.ui_automation.get_text()

    def get_parsed_text(self, environment: str, text: str) -> ReportNode:
        """
        Method used to get the parsed text from the NLP and hinter via the server
        :param environment: The current environment the Radiologist is working in
        :param text: The text that needs to be parsed
        """
        data = {"text": text}
        res = requests.get("http://127.0.0.1:5000/mammo/", json=data)
        return jsonpickle.decode(res.json()["Data"])

    def get_parsed_text_temp(self, environment: str, text: str) -> ReportNode:
        """
        Send the text to the server to retrieve a ReportTree.
        :param environment: The environment that should interpret the text.
        :param text: The text to be interpreted.
        :return: A ReportNode containing the desired structure.
        """
        # TODO: This is a temporary
        with open('TESTPICKLE.pkl', 'rb') as file:
            return pickle.load(file)


if __name__ == "__main__":
    c = Controller(UIAutomation())
    tree = c.get_parsed_text_temp('', '')
    newtree = c.get_parsed_text("mammo", "X-mammografie beiderzijds: Een "
                                "stervormige laesie laterale bovenkwadrant linkermamma")
    print("end")
