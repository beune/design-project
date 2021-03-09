"""
Imports
"""


class ReportLeaf:
    """
    Class used to represent Nodes
    """
    def __init__(self, text: str, label: str, certainty: float, hint: str = None):
        self._text = text
        self._label = label
        self._certainty = certainty
        self._hint = hint

    def __repr__(self):
        return 'Leaf("{}", {}, {})'.format(self._text, self._label, self._certainty)

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.text == other.text \
               and self.label == other.label \
               and self.certainty == other.certainty

    @property
    def text(self):
        """

        :return: Returns the text of the report leaf
        """
        return self._text

    @property
    def label(self):
        """

        :return: Returns the label of the report leaf
        """
        return self._label

    @property
    def certainty(self):
        """

        :return: Returns the certainty of the labelling of the leaf
        """
        return self._certainty

    @property
    def hint(self):
        """

        :return: Returns the hint of the leaf
        """
        return self._hint
