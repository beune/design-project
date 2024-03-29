"""
File used to connect Shreyasi's python2 algorithm to python 3
"""
from typing import List, Tuple
import json

import os
import xml.etree.ElementTree as ElementTree
from xml.dom import minidom

from reporttree.label_node import LabelNode
from reporttree.node import Node

COLOURS = {
    "breast composition": "#E71212",
    "shape": "#E77C12",
    "margin": "#EDED12",
    "size": "#13EB13",
    "location": "#13EBEB",
    "morphology": "#1313EB",
    "associated_features": "#D981D9",
    "distribution": "#81ADD9",
    "architectural_distortion": "#A9C9CF",
}

COMM = "python2 \"./nlp/AutomaticStructuring/CRF Model A/predict_labels.py\""
PATH = "./nlp"

SCRIPT = "./AutomaticStructuring/CRF MODEL A/predict_labels.py"

INPUT_FILE = "/AutomaticStructuring/data/testSample_input.xml"
OUTPUT_FILE = "/AutomaticStructuring/data/out.json"

HINTS = {
    "breast composition": "In the BI-RADS edition 2013 the assignment of the breast composition is changed into a, b, c"
                          "and d-categories followed by a description: \n"
                          "- A The breast are almost entirely fatty. Mammography is highly sensitive in this setting.\n"
                          "- B There are scattered areas of fibroglandular density. The term density describes the degr"
                          "ee of x-ray attenuation of breast tissue but not discrete mammographic findings.\n"
                          "- C The breasts are heterogeneously dense, which may obscure small masses."
                          "Some areas in the breasts are sufficiently dense to obscure small masses.\n"
                          "- D The breasts are extremely dense, which lowers the sensitivity of mammography",
    "shape": "oval-round-irregular",
    # "margin": "The margin of the mass",
    "margin": "The margin of the mass. The margin of a mass can be:\n"
              "-Circumscribed \n"
              "-Obscured or partially obscured\n"
              "-Microlobulated. This implies a suspicious finding.\n"
              "-Indistinct\n"
              "-Spiculated with radiating lines from the mass is a very suspicious finding.\n",
    "location": "The location of the mass",
    "size": "The size of the mass",
    "density": "fat-low-equal-high",
    "mass": " A Mass is a space occupying 3D lesion seen in two different projections."
            "If a potential mass is seen in only a single projection it should be called a 'asymmetry' until its three-"
            "dimensionality is confirmed.\n"
            "- Shape: oval (may include 2 or 3 lobulations), round or irregular\n"
            "- Margins: circumscribed, obscured, microlobulated, indistinct, spiculated\n"
            "- Density: high, equal, low or fat-containing.\n"
}

EXPECTED_LEAVES = {
    "report": {
        "positive_finding": {
            "mass": ["shape", "margin", "density"],
            "calcification": ["morphology", "distribution"],
        }
    }
}


OPTIONS = {
    "shape": ["oval", "round", "irregular"],
    "margin": ["circumscribed", "obscured", "microlobulated", "indistinct", "spiculated"],
    "density": ["fat", "low", "equal", "high"],
    "asymmetry": ["asymmetry", "global", "focal", "developing"],
    "morphology": ["typically benign", "amorphous", "coarse heterogeneous", "fine pleiomorphic", "fine linear or fine "
                                                                                                 "linear branching"],
    "distribution": ["diffuse", "regional", "grouped", "linear", "segmental"],
}


def parse(text):
    """
    Method used to process the new incoming text
    :param text: The new text of the model
    """
    make_input(text)
    run()
    tree, _, _ = make_tree([], get_list())
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
    xml_string = minidom.parseString(ElementTree.tostring(top)).toprettyxml()
    with open(os.path.normpath(PATH + INPUT_FILE), "w") as f:
        f.write(xml_string)


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
        return json.load(file)


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
    return (label_after.startswith('I-') and len(label_before) > 2
            and label_after[2:] == label_before[2:] or label_before == label_after == 'O')


def clean(unfiltered: str) -> str:
    """
    Function for standardising labels
    :param unfiltered: string containing B and I flags
    :return: the filtered string without the flags
    """
    if unfiltered.startswith("I-") or unfiltered.startswith("B-"):
        return unfiltered[2:]
    return unfiltered


def make_tree(base: List[str], items: list) -> Tuple[Node, List[str], float]:
    """
    Make a tree based on a linear list of items
    :param base: the category of created Node
    :param items: items left for processing. Will be mutated!
    :return: the created Node, the text of the node and the confidence
    """
    base_length = len(base)
    agg_text = []
    sum_conf = 0
    count = 0
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
            count += 1
            items.pop(0)
        # the new label should not be ignored
        else:
            # make a new tree that has a base that goes one label deeper
            child, child_agg_text, child_sum_conf = make_tree(labels[:base_length + 1], items)
            children.append(child)
            agg_text += child_agg_text
            sum_conf += child_sum_conf

    category = clean(base[-1]) if base else 'report'
    if not agg_text:
        return Node(category, children=children), agg_text, sum_conf

    pred_text = ' '.join(agg_text)
    conf = int(sum_conf / len(agg_text) * 100)
    if category in OPTIONS:
        return LabelNode(category, OPTIONS[category], text_prediction=(pred_text, conf)), agg_text, sum_conf
    return Node(category, text_prediction=(pred_text, conf), children=children), agg_text, sum_conf


def add_labels(node: Node):
    """
    Add labels with confidences to the leaves in the tree.
    :type node: ReportNode
    """
    for child in node:
        if isinstance(child, LabelNode):
            child.pred_label = child.text
            child.pred_label_conf = 70
        add_labels(child)
