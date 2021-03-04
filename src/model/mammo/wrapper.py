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


class Wrapper(NLP):
    """
    Class used to connect Shreyasi's python2 algorithm to python 3
    """
    COMMAND = "python --version"

    @classmethod
    def process(cls, text):
        """
        Method used to process the new incoming text
        :param text: The new text of the model
        """
        return os.system(cls.COMMAND)

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

    def format(self, problist):
        """
        Structure 1 to structure 2 converter
        :param problist:
        :return:
        """
        # TODO: implement format conversion (special class?)
        return problist


if __name__ == "__main__":
    w = Wrapper()
    out = w.process("X-mammografie beiderzijds: Een stervormige laesie laterale bovenkwadrant linkermamma, De laesie "
                    "heeft een body van ongeveer 2,3 cm, De laesie is wel moeilijk af te grenzen van het normale "
                    "klierweefsel,  In en rondom de laesie geen microcalcificaties, In de rechtermamma voor zover te "
                    "beoordelen geen aanwijzingen voor maligniteit, Axillair beiderzijds geen pathologische "
                    "lymfeklieren zichtbaar")
    print(out)
