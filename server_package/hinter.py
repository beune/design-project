"""
Imports
"""
from typing import List, Dict

from reporttree.label_node import LabelNode
from reporttree.node import Node


class Hinter:
    """
    Generic Class for addition of hints to NLP outcome
    """

    def __init__(self, expected_leaves: Dict[str, List[str]], labels: Dict[str, List[str]], hints: Dict[str, str]):
        self.expected_leaves = expected_leaves
        self.labels = labels
        self.hints = hints

    def hint(self, node: Node):
        """
        Method used recursively to add hints and expectations to nodes in the node structure
        :param node: The node for which the hints and expectations should be added
        """
        if node.category in self.expected_leaves:
            found = [child.category for child in node]
            for category in self.expected_leaves[node.category]:
                if category not in found:
                    if category in self.labels:
                        leaf = LabelNode(category, self.labels[category])
                    else:
                        leaf = Node(category)
                    node.add_child(leaf)
        for child in node:
            if child.category in self.hints:
                child.hint = self.hints[child.category]
            self.hint(child)
