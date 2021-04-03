"""
Classes used for user changes to the tree
"""


class BackChange:
    """
    Class used to store a user change and apply it to the tree
    """
    def __init__(self, label: str = None, text: str = None):
        self.label = label
        self.text = text


class FrontChange:
    """
    Class used to store a change only relevant to the frontend
    """
    def __init__(self, warning: bool = None):
        self.warning = warning
