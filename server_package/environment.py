"""
Imports
"""
from reporttree.node import Node

from server_package.environments import hersen, mammo, mammo_fw
from server_package.hinter import Hinter
from typing import Callable


class Environment:
    """
    Class for environments
    """

    def __init__(self, name: str, parse: Callable[[str], Node], colours: dict, hinter: Hinter = None):
        """
        Initialize environment object
        :param name: the name of the environment
        :param parse: the text parser
        :param colours: the colours for each category
        :param hinter: an optional hinter
        """
        self.parse = parse
        self.colours = colours
        self.hinter = hinter
        self.name = name

    def process(self, text: str) -> Node:
        """
        Method used to process text and hint the resulting tree
        :param text: the text that should be processed
        :return: the resulting tree
        """
        processed = self.parse(text)
        if self.hinter:
            self.hinter.hint(processed, self.hinter.expected_leaves)
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
