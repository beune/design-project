"""
Imports
"""
from structure import Structure
from hinter import Hinter
from nlp import NLP


class Environment(object):
    """
    Environment class which is interchangeable for different types of radiology
    Each environment contains:
        - Natural Language Processer, used to process the natural language into labelled XML
        - Structure, used to generate a user-friendly structure out of the XML
        - Hinter, used to provide hints based on the current XML
    """
    def __init__(self, nlp: NLP, structure: Structure, hinter: Hinter):
        self.nlp = nlp
        self.structure = structure
        self.hinter = hinter

    @property
    def nlp(self) -> NLP:
        """
        Method used to retrieve the current Natural Language Processing algorithm that is used
        :return: The current NLP algorithm
        """
        return self.nlp

    @property
    def structure(self) -> Structure:
        """
        Method used to retrieve the current structure that is used
        :return: The current structuring algorithm
        """
        return self.structure

    @property
    def hinter(self) -> Hinter:
        """
        Method used to retrieve the current hinter that is used
        :return: The current hinting algorithm
        """
        return self.hinter
