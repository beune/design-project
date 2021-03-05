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

    def add_replacement(self, key: str, replacement: str) -> None:
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
        if self.replacements.keys():
            for key in self.replacements.keys():
                new_text = re.sub(key, self.replacements[key], text, flags=re.I)
            return new_text
        else:
            return text

    def switch_replacements(self, reps: dict) -> None:
        """
        Method used to switch the replacements when switched between environments
        :param reps: the new replacements
        """
        self.replacements = reps

    def remove_replacement(self, key):
        """
        Method used to remove a replacement
        :param key: The key of the replacement which needs to be removed
        """
        try:
            del self.replacements[key]
        except KeyError:
            pass


if __name__ == "__main__":
    x = Replacer()
    x.add_replacement("Uitslag besproken", "Uitslag telefonisch doorgebeld")
    print(x.replace("uitslag besproken, Alles goedgegaan"))
    x.remove_replacement("Uitslag besproken")
    print(x.replace("uitslag besproken, Alles goedgegaan"))
