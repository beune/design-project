"""
Imports
"""


class ReportNode:
    """
    Class used to represent Nodes
    """
    def __init__(self, label: str, children: list = None, expects: list = None):
        self.label = label
        self.children = [] if children is None else children
        self.expects = [] if expects is None else expects

    def __repr__(self):
        return 'Node({})'.format(self.label)

    def __iter__(self):
        for child in self.children:
            yield child

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.label == other.label \
               and self.children == other.children

    def get_child(self, index):
        """
        Method used to get a child of a node based on it's index
        If there's no child at the given index, raise a keyError
        :param index: The index of the requested child
        :return: The child node at the given index
        """
        return self.children[index]

    def add_child(self, child):
        """
        Method used to update the children of a ReportNode
        :param child: The new child that needs to be added to the children list
        """
        self.children.append(child)
