"""
Imports
"""
from typing import List, Tuple
import json
import platform

from src.model.nlp import NLP
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from src.model.report_node import ReportNode
from src.model.report_leaf import ReportLeaf

import re


# def split_on_common(new, old):
#     if not old or not new:
#         return [], new
#     for (i, (new_label, old_label)) in enumerate(zip(new, old)):
#         if new_label != old_label:
#             return new[:i], new[i:]
#     return new[:i+1], new[i+1:]
#
# def split(new, old):
#     if not new or not old or new[0] != old[0]:
#         return 0
#     else:
#     # elif new[0] == old[0]:
#         return 1 + split(new[1:], old[1:])
#     # else:
#     #     return 1


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

    def process(self, text):
        """
        Method used to process the new incoming text
        :param text: The new text of the model
        """
        self.make_input(text)
        self.run()
        return self.format(self.get_list())

    def make_input(self, text: str) -> None:
        """
        Method used to transform the current string into the correct XML format for the classifying algorithm
        :param text: The current string of the report
        """
        top = ET.Element('radiology_reports')
        child = ET.SubElement(top, 'report')
        child.text = text
        xmlstr = minidom.parseString(ET.tostring(top)).toprettyxml()
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

    def format(self, problist) -> ReportNode:
        """
        Structure 1 to structure 2 converter
        :param problist:
        :return:
        """
        def filter(unfiltered: str) -> str:
            """
            Function for standardising labels
            :param unfiltered: string containing B and I flags
            :return: the filtered string
            """
            return re.sub(r'(I-|B-)', '', unfiltered)

        # convert to a linear form
        # unlabeled text is removed and consecutive words with the same labels are combined
        agg_text, last_label, sum_conf, count = '', None, 0, 1  # default values
        linear = []
        for (text, label_text, conf) in problist:
            top_label = label_text.split('/')[-1]
            if top_label.startswith('I-'):
                # aggregate
                agg_text += ' ' + text
                sum_conf += conf
                count += 1
            elif top_label != 'O':
                # add
                if last_label is not None:
                    agg_conf = sum_conf / count
                    linear.append((agg_text, last_label, agg_conf))
                # reset
                last_label = filter(label_text)
                agg_text, sum_conf = text, conf
                count = 1
        # final add
        agg_conf = sum_conf / count
        linear.append((agg_text, last_label, agg_conf))

        # convert linear form to a tree
        root = ReportNode("root")
        for (text, label_text, conf) in linear:
            node = root
            labels = label_text.split("/")
            for label in labels[:-1]:
                node = node.get_or_create(label)
            node.add_child(ReportLeaf(text, labels[-1], conf))
        # TODO: B/I only works for top_label
        return root

    def maketree(self, labels, text, node: ReportNode, conf):
        """

        :param labels:
        :param text:
        :param node:
        :param conf:
        """
        if len(labels) <= 2:
            node.add_child(ReportLeaf(text, labels[0], conf))
        else:
            flag, label = labels[0].split('-', 1)
            # if there was no flag
            if label is None:
                flag, label = label, flag
            # if flag == 'I':
            #     self._recent[label].add2(labels[1:], text, conf)
            else:
                newnode = ReportNode(label)
                self.maketree(labels[1:], text, newnode, conf)
                node.add_child(newnode)
                # self._recent[label] = newnode


if __name__ == "__main__":
    w = Wrapper()
    # out = w.process("X-mammografie beiderzijds: Een stervormige laesie laterale bovenkwadrant linkermamma, De laesie "
    #                 "heeft een body van ongeveer 2,3 cm, De laesie is wel moeilijk af te grenzen van het normale "
    #                 "klierweefsel,  In en rondom de laesie geen microcalcificaties, In de rechtermamma voor zover te "
    #                 "beoordelen geen aanwijzingen voor maligniteit, Axillair beiderzijds geen pathologische "
    #                 "lymfeklieren zichtbaar")
    # print(out)
    # print(split_on_common([1, 2, 4], []))
    # print(split([1, 2, 4], [1, 2, 4]))
    with open("..\\out.json", "r") as file:
        problist = json.load(file)
    out = w.format(problist)
    print("Succes")
