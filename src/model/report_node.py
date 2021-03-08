"""
Imports
"""


class ReportNode:
    """
    Class used to represent Nodes
    """
    def __init__(self, label: str):
        self._label = label
        self._children = []

    def __repr__(self):
        return 'Node({})'.format(self._label)

    @property
    def label(self) -> str:
        """

        :return:
        """
        return self._label

    @property
    def children(self) -> list:
        """

        :return:
        """
        return self._children

    @property
    def expects(self) -> list:
        """

        :return:
        """
        return self._expects

    def add_child(self, child):
        """
        Method used to update the children of a ReportNode
        :param child: The new child that needs to be added to the children list
        """
        self._children.append(child)
