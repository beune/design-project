"""
Imports
"""
import re


class Replacer(object):
    """
    Class used to replace certain strings with standardized strings
    """

    def __init__(self):
        self.replacements = {}

    def set_replacement(self, key: str, replacement: str) -> None:
        """
        Function used to
        :param key: The standard string which needs to be replaced
        :param replacement: The string which functions as the replacement
        """
        self.replacements[key] = replacement

    def replace(self, text: str) -> str:
        """
        Method used to replace the necessary parts of the text
        :param text: The text which needs to be checked for replacement possibilities
        """
        return self.check_replacements(text)

    def check_replacements(self, text: str) -> str:
        """
        Method used to check for replacements in the text of a label.
        :param text: The text of a label
        """
        new_text = ""
        for key in self.replacements.keys():
            new_text = re.sub(key.lower(), self.replacements[key], text.lower())
        return new_text

    def switch_replacements(self, reps: dict) -> None:
        """
        Method used to switch the replacements when switched between environments
        :param reps: the new replacements
        """
        self.replacements = reps
