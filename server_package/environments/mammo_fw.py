"""
File used to connect Shreyasi's python2 algorithm to python 3 and labels with FuzzyWuzzy
"""
from fuzzywuzzy import process
from reporttree.label_node import LabelNode
from reporttree.node import Node

import server_package.environments.mammo as mammo

OPTIONS = mammo.OPTIONS

HINTS = mammo.HINTS

COLOURS = mammo.COLOURS

EXPECTED_LEAVES = mammo.EXPECTED_LEAVES


def parse(text) -> Node:
    """
    Method used to process the new incoming text
    :param text: The new text of the model
    """
    mammo.make_input(text)
    mammo.run()
    tree, _, _ = mammo.make_tree([], mammo.get_list())
    add_labels(tree)
    return tree


def add_labels(node: Node) -> None:
    """
    Add labels with confidences to the leaves in the tree using FuzzyWuzzy.
    :type node: ReportNode
    """
    for child in node:
        if isinstance(child, LabelNode) and child.category in OPTIONS:
            child.pred_label, child.pred_label_conf = process.extractOne(child.text, OPTIONS[child.category])
        add_labels(child)
