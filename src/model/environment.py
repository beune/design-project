"""
Imports
"""
from hinter import Hinter
from nlp import NLP


class Environment(object):
    """
    Environment class which is interchangeable for different types of radiology
    Each environment contains:
        - Natural Language Processer, used to process the natural language into labelled XML
        - Hinter, used to provide hints based on the current XML
    """
    def __init__(self, nlp: NLP, hinter: Hinter):
        self.nlp = nlp
        self.hinter = hinter
