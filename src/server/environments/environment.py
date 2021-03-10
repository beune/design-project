"""
Imports
"""
from src.model.report_node import ReportNode
from src.server.environments.hersen import hersen, hersenhinter
from src.server.environments.mammo import mammohinter
from src.server.environments.mammo import wrapper
from typing import Callable


class Environment:
    """
    Class for environments
    """

    def __init__(self, parse: Callable, hint: Callable = None):
        self.parse = parse
        self.hint = hint

    def process(self, text: str) -> ReportNode:
        """
        Method used to process text
        :param text:
        :return:
        """
        processed = self.parse(text)
        if self.hint:
            self.hint(processed)
        return processed


envs = {
    "mammo": Environment(wrapper.parse, mammohinter.hint),
    "hersen": Environment(hersen.parse, hersenhinter.hint),
}
