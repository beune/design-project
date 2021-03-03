"""
Imports
"""
from src.model.nlp import NLP
import os


class Wrapper(NLP):
    """
    Class used to connect Shreyasi's python2 algorithm to python 3
    """
    COMMAND = "python --version"

    @classmethod
    def process(cls, text):
        """

        :param text:
        """
        return os.system(cls.COMMAND)


if __name__ == "__main__":
    print(Wrapper.process("Hallo"))
