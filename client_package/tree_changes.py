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
    def __init__(self, text_warning: bool = None, label_warning: bool = None):
        self.text_warning = text_warning
        self.label_warning = label_warning
