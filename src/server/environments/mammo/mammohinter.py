"""
Imports
"""
from src.model.report_leaf import ReportLeaf
from src.model.report_node import ReportNode

hints = {
    "shape": "oval-round-irregular",
    "margin": "The margin of the mass",
    "density": "fat-low-equal-high",
}

expected = {
    "mass": ["shape", "margin", "density"],
    "calcifications": ["morphology", "distribution"]
}


def hint(node: ReportNode):
    """

    :param node:
    """
    if node.label in expected:
        node.expects = expected[node.label]
    for child in node:
        if isinstance(child, ReportNode):
            hint(child)
        elif isinstance(child, ReportLeaf):
            hint_leaf(child)
        else:
            raise Exception("huh")


def hint_leaf(leaf: ReportLeaf):
    """

    :param leaf:
    """
    if leaf.label in hints:
        leaf.hint = hints[leaf.label]
