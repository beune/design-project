"""
Imports
"""
from report_tree.report_node import ReportNode
from src.server.environments import hersen, mammo
from src.server.hinter import Hinter
from typing import Callable


class Environment:
    """
    Class for environments
    """

    def __init__(self, parse: Callable, hinter: Hinter = None):
        self.parse = parse
        self.hinter = hinter

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


envs = {
    "mammo": Environment(mammo.parse, Hinter(mammo.expected, mammo.hints)),
    "hersen": Environment(hersen.parse, Hinter(hersen.expected, hersen.hints)),
}
