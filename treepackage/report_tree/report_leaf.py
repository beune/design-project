"""
Imports
"""


class ReportLeaf:
    """
    Class used to represent Leaves
    """
    def __init__(self, text: str, label: str, certainty: float, hint: str = None):
        self.text = text
        self.label = label
        self.certainty = certainty
        self.hint = hint

    def __repr__(self):
        return 'Leaf("{}", {}, {})'.format(self.text, self.label, self.certainty)

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.text == other.text \
               and self.label == other.label \
               and self.certainty == other.certainty
