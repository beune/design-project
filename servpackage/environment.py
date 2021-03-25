"""
Imports
"""
from report_tree.report_node import ReportNode
from servpackage.environments import hersen, mammo
from servpackage.hinter import Hinter
from typing import Callable


class Environment:
    """
    Class for environments
    """

    def __init__(self, name: str, parse: Callable, colours: dict, hinter: Hinter = None):
        """
        Initialize environment object
        :param name: the name of the environment (as it is presented in front end)
        :param colours:
        :param parse:
        :param hinter:
        """
        self.parse = parse
        self.colours = colours
        self.hinter = hinter
        self.name = name

    def process(self, text: str) -> ReportNode:
        """
        Method used to process text
        :param text:
        :return:
        """
        processed = self.parse(text)
        if self.hinter:
            self.hinter.hint(processed)
        return processed


ENVS = {
    "mammo": Environment("Mammo", mammo.parse, mammo.COLOURS, Hinter(mammo.expected, mammo.hints)),
    "hersen": Environment("Hersen", hersen.parse, hersen.COLOURS, Hinter(hersen.expected, hersen.hints))
}
