"""
Imports
"""
from report_tree.report_node import ReportNode
from server_package.environments import hersen, mammo, mammo_fw
from server_package.hinter import Hinter
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
    "mammo": Environment(
        name="Mammo",
        parse=mammo.parse,
        colours=mammo.COLOURS,
        hinter=Hinter(mammo.EXPECTED_LEAVES, mammo.OPTIONS, mammo.HINTS)
    ),
    "mammo_fw": Environment(
        name="Mammo Fuzzy Wuzzy",
        parse=mammo_fw.parse,
        colours=mammo_fw.COLOURS,
        hinter=Hinter(mammo_fw.EXPECTED_LEAVES, mammo_fw.OPTIONS, mammo_fw.HINTS)
    ),
    "hersen": Environment(
        name="Hersen",
        parse=hersen.parse,
        colours=hersen.COLOURS,
        hinter=Hinter(hersen.EXPECTED, hersen.OPTIONS, hersen.HINTS)
    ),
}