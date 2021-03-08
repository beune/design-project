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
    def certainty(self):
        """

        :return:
        """
        return self._certainty
