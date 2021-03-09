"""
Imports
"""


class ReportNode:
    """
    Class used to represent Nodes
    """
    def __init__(self, label: str, children: list = None, expects: list = None):
        self._label = label
        self._children = [] if children is None else children
        self._expects = expects

    def __repr__(self):
        return 'Node({})'.format(self._label)

    def __iter__(self):
        for child in self._children:
            yield child

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
