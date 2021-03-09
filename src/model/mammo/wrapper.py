"""
Imports
"""
from typing import List, Tuple
import json
import platform

from src.model.nlp import NLP
import os
import xml.etree.ElementTree as ElementTree
from xml.dom import minidom

from src.model.report_node import ReportNode
from src.model.report_leaf import ReportLeaf

import re


class Wrapper(NLP):
    """
    Class used to connect Shreyasi's python2 algorithm to python 3
    """
    COMMAND = 'cd "{}" \n{}\npython2 "{}"\n'
    # PATH = "../nlpbreastcancer/"
    PATH = "C:/Users/voetb/OneDrive/Documenten/Mod11/nlpbreastcancer/"
    WIN_VENV = ".\\venv\\Scripts\\activate"
    LINUX_VENV = "source ./venv/bin/activate"

    SCRIPT = "./AutomaticStructuring/CRF MODEL A/predict_labels.py"

    INPUT_FILE = "./AutomaticStructuring/data/testSample_input.xml"
    OUTPUT_FILE = "./AutomaticStructuring/data/out.json"

    # TODO: Create init met path als argument?

    def process(self, text):
        """
        Method used to process the new incoming text
        :param text: The new text of the model
        """
        self.make_input(text)
        self.run()
        return make_tree([], self.get_list())

    def make_input(self, text: str) -> None:
        """
        Method used to transform the current string into the correct XML format for the classifying algorithm
        :param text: The current string of the report
        """
        top = ElementTree.Element('radiology_reports')
        child = ElementTree.SubElement(top, 'report')
        child.text = text
        xmlstr = minidom.parseString(ElementTree.tostring(top)).toprettyxml()
        with open(os.path.normpath(self.PATH + self.INPUT_FILE), "w") as f:
            f.write(xmlstr)

    def run(self) -> None:
        """
        Method used to run the classifying algorithm
        """
        path = os.path.normpath(self.PATH)
        system = platform.system()
        if system == 'Windows':
            venv = self.WIN_VENV
        elif system == 'Linux':
            venv = self.LINUX_VENV
        else:
            raise Exception('Unsupported OS')
        script = os.path.normpath(self.SCRIPT)
        command = self.COMMAND.format(path, venv, script)
        os.system(command)

    def get_list(self) -> List[Tuple[str, str, float]]:
        """
        Method used to get the list of words and their certainties
        :return A list of lists in the format: [[word, label, probability]]
        """
        with open(os.path.normpath(self.PATH + self.OUTPUT_FILE), "r") as file:
            problist = json.load(file)
        return problist


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
    # TODO: The second check is probably obsolete; All labels need to start with B- or I-
    # TODO: Do we need to check if the label_before has enough characters?
    return label_after.startswith('I-') and len(label_before) > 2 and label_after[2:] == label_before[2:] \
        or not label_after.startswith('B-') and label_after == label_before


def clean(unfiltered: str) -> str:
    """
    Function for standardising labels
    :param unfiltered: string containing B and I flags
    :return: the filtered string without the flags
    """
    return re.sub(r"(I-|B-)", '', unfiltered)


def make_tree(base: list[str], items: list):
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

        # the base equals the labels, collect all the text and confidences
        if base_length == len(labels):
            agg_text.append(text)
            sum_conf += conf
            items.pop(0)
        # the new label should not be ignored
        elif labels[base_length] != 'O':
            # make a new tree that has a base that goes one label deeper
            child = make_tree(labels[:base_length + 1], items)
            children.append(child)
        # the new label should be ignored
        else:
            items.pop(0)

    report_label = clean(base[-1]) if base else 'root'
    # if text has been found create a Leaf, otherwise a node
    if agg_text:
        return ReportLeaf(' '.join(agg_text), report_label, sum_conf / len(agg_text))
    return ReportNode(report_label, children)


if __name__ == "__main__":
    w = Wrapper()
    # out = w.process("X-mammografie beiderzijds: Een stervormige laesie laterale bovenkwadrant linkermamma, De laesie "
    #                 "heeft een body van ongeveer 2,3 cm, De laesie is wel moeilijk af te grenzen van het normale "
    #                 "klierweefsel,  In en rondom de laesie geen microcalcificaties, In de rechtermamma voor zover te "
    #                 "beoordelen geen aanwijzingen voor maligniteit, Axillair beiderzijds geen pathologische "
    #                 "lymfeklieren zichtbaar")
    with open("..\\out.json", "r") as file:
        problist = json.load(file)
    out = make_tree([], problist)
    print(out)
