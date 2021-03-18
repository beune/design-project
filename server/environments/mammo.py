"""
Imports
"""
from typing import List, Tuple
import json

import os
import xml.etree.ElementTree as ElementTree
from xml.dom import minidom

from report_tree.report_node import ReportNode
from report_tree.report_leaf import ReportLeaf

"""
Class used to connect Shreyasi's python2 algorithm to python 3
"""
COMM = "python2 \"./nlp/AutomaticStructuring/CRF Model A/predict_labels.py\""
PATH = "./nlp"

SCRIPT = "./AutomaticStructuring/CRF MODEL A/predict_labels.py"

INPUT_FILE = "/AutomaticStructuring/data/testSample_input.xml"
OUTPUT_FILE = "/AutomaticStructuring/data/out.json"

hints = {
    "shape": "oval-round-irregular",
    "margin": "The margin of the mass",
    "density": "fat-low-equal-high",
}

expected = {
    "mass": ["shape", "margin", "density"],
    "calcifications": ["morphology", "distribution"]
}

options = {
    "shape": ["oval", "round", "irregular"],
    "margin": ["circumscribed", "obscured", "microlobulated", "indistinct", "spiculated"],
    "density": ["fat", "low", "equal", "high"],
    "asymmetry": ["asymmetry", "global", "focal", "developing"],
    "morphology": ["typically benign", "amorphous", "coarse heterogeneous", "fine pleiomorphic", "fine linear or fine "
                                                                                                 "linear branching"],
    "distribution": ["diffuse", "regional", "grouped", "linear", "segmental"],
}

alternatives = {key: {label: 0 for label in option_list} for key, option_list in options.items()}


def parse(text):
    """
    Method used to process the new incoming text
    :param text: The new text of the model
    """
    make_input(text)
    run()
    tree = make_tree([], get_list())
    add_labels(tree)
    return tree


def make_input(text: str) -> None:
    """
    Method used to transform the current string into the correct XML format for the classifying algorithm
    :param text: The current string of the report
    """
    top = ElementTree.Element('radiology_reports')
    child = ElementTree.SubElement(top, 'report')
    child.text = text
    xmlstr = minidom.parseString(ElementTree.tostring(top)).toprettyxml()
    with open(os.path.normpath(PATH + INPUT_FILE), "w") as f:
        f.write(xmlstr)


def run() -> None:
    """
    Method used to run the classifying algorithm
    """
    os.system(os.path.normpath(COMM))


def get_list() -> List[Tuple[str, str, float]]:
    """
    Method used to get the list of words and their certainties
    :return A list of lists in the format: [[word, label, probability]]
    """
    with open(os.path.normpath(PATH + OUTPUT_FILE), "r") as file:
        data = json.load(file)
    return data


def has_base(labels, base) -> bool:
    """
    Check if the labels are a descendant from base.
    :param labels: the labels that is checked to have a base.
    :param base: the base to be compared with.
    :return: true if all labels came after base. See after for what is defined as after.
    """
    if len(labels) < len(base):
        return False
    for label_a, label_b in zip(labels, base):
        if not after(label_a, label_b):
            return False
    return True


def after(label_after: str, label_before: str) -> bool:
    """
    Check if label_after is indeed expected after label_before.
    These labels cannot start with B- and, apart from flag, should be equal
    :param label_after: the label that comes afterwards
    :param label_before: the label that comes first
    :return: true if the label can come afterwards
    """
    return label_after.startswith('I-') and len(label_before) > 2 and label_after[2:] == label_before[2:] \
        or label_before == label_after == 'O'


def clean(unfiltered: str) -> str:
    """
    Function for standardising labels
    :param unfiltered: string containing B and I flags
    :return: the filtered string without the flags
    """
    if unfiltered.startswith("I-") or unfiltered.startswith("B-"):
        return unfiltered[2:]
    return unfiltered


def make_tree(base: List[str], items: list):
    """
    Make a tree based on a linear list of items.
    :param base:
    :param items: items left for processing. Will be mutated!
    :return:
    """
    base_length = len(base)
    agg_text = []
    sum_conf = 0
    children = []
    first = True
    # loop while items exist and the current label descents from the base (break statement)
    while items:
        (text, label_text, conf) = items[0]
        labels = label_text.split("/")
        # break if the label has a new base
        if not first and not has_base(labels, base):
            break
        # make sure that only the first B-flag is ignored
        first = False

        # the base equals the alternatives, collect all the text and confidences
        if base_length == len(labels):
            agg_text.append(text)
            sum_conf += conf
            items.pop(0)
        # the new label should not be ignored
        else:
            # make a new tree that has a base that goes one label deeper
            child = make_tree(labels[:base_length + 1], items)
            children.append(child)
        # the new label should be ignored

    category = clean(base[-1]) if base else 'root'
    # if text has been found create a Leaf, otherwise a node
    if agg_text:
        conf = sum_conf / len(agg_text)
        return ReportLeaf(' '.join(agg_text), category, conf)
    return ReportNode(category, children)


def add_labels(node: ReportNode):
    """
    Add labels with confidences to the leaves in the tree.
    :type node: ReportNode
    """
    for child in node:
        if isinstance(child, ReportNode):
            add_labels(child)
        elif isinstance(child, ReportLeaf) and child.key in alternatives:
            child.labels = alternatives[child.key]


if __name__ == '__main__':
    # Generate a pickle file containing a test tree using json as input
    with open("out.json", "r") as json_file:
        data = json.load(json_file)
    tree = make_tree([], data)
    add_labels(tree)
    import pickle
    with open("TESTPICKLE.pkl", "wb") as tree_file:
        pickle.dump(tree, tree_file)
