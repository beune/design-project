"""
File used to connect Shreyasi's python2 algorithm to python 3 and labels with FuzzyWuzzy
"""
from fuzzywuzzy import process
from report_tree.report_leaf import LabelLeaf
from report_tree.report_node import ReportNode

import server_package.environments.mammo as mammo

OPTIONS = mammo.OPTIONS

HINTS = mammo.HINTS

COLOURS = mammo.COLOURS

EXPECTED_LEAVES = mammo.EXPECTED_LEAVES


def parse(text):
    """
    Method used to process the new incoming text
    :param text: The new text of the model
    """
    mammo.make_input(text)
    mammo.run()
    tree = mammo.make_tree([], mammo.get_list())
    add_labels(tree)
    return tree


def add_labels(node: ReportNode):
    """
    Add labels with confidences to the leaves in the tree using FuzzyWuzzy.
    :type node: ReportNode
    """
    for child in node:
        if isinstance(child, ReportNode):
            add_labels(child)
        elif isinstance(child, LabelLeaf) and child.field in OPTIONS:
            child.label, percentage = process.extractOne(child.text, OPTIONS[child.field])
            child.conf = percentage/100
