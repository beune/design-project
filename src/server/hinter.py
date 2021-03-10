"""
Imports
"""
from src.report_leaf import ReportLeaf
from src.report_node import ReportNode
from typing import List, Dict


class Hinter:
    """
    Generic Class for addition of hints to NLP outcome
    """

    def __init__(self, expected: Dict[str, List[str]], hints: Dict[str, List[str]]):
        self.expected = expected
        self.hints = hints

    def hint(self, node: ReportNode):
        """
        Method used recursively to add hints and expectations to nodes in the node structure
        :param node: The node for which the hints and expectations should be added
        """
        if node.label in self.expected:
            node.expects = self.expected[node.label]
        for child in node:
            if isinstance(child, ReportNode):
                self.hint(child)
            elif isinstance(child, ReportLeaf):
                self.hint_leaf(child)

    def hint_leaf(self, leaf: ReportLeaf):
        """
        Method used to add hints to leafs
        :param leaf: The leaf for which the hint needs to be added
        """
        if leaf.label in self.hints:
            leaf.hint = self.hints[leaf.label]
