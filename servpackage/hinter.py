"""
Imports
"""
from report_tree.report_leaf import TextLeaf, LabelLeaf
from report_tree.report_node import ReportNode
from typing import List, Dict, Set


class Hinter:
    """
    Generic Class for addition of hints to NLP outcome
    """

    def __init__(self, expected_leaves: Dict[str, List[str]], labels: Dict[str, Set[str]], hints: Dict[str, str]):
        self.expected_leaves = expected_leaves
        self.labels = labels
        self.hints = hints

    def hint(self, node: ReportNode):
        """
        Method used recursively to add hints and expectations to nodes in the node structure
        :param node: The node for which the hints and expectations should be added
        """
        if node.category in self.expected_leaves:
            found = [child.field for child in node if isinstance(child, TextLeaf)]
            for field in self.expected_leaves[node.category]:
                if field not in found:
                    if field in self.labels:
                        leaf = LabelLeaf(field, self.labels[field])
                    else:
                        leaf = TextLeaf(field)
                    node.add_child(leaf)
        for child in node:
            if isinstance(child, ReportNode):
                self.hint(child)
            elif isinstance(child, TextLeaf):
                self.hint_leaf(child)

    def hint_leaf(self, leaf: TextLeaf):
        """
        Method used to add hints to leafs
        :param leaf: The leaf for which the hint needs to be added
        """
        if leaf.field in self.hints:
            leaf.hint = self.hints[leaf.field]
