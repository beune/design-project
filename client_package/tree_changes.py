"""
Classes used for storing changes to nodes
"""


class BackChange:
    """
    Class used to store a user change to nodes
    """
    def __init__(self, label: str = None, text: str = None):
        self.label = label
        self.text = text


class FrontChange:
    """
    Class used to store front-end changes
    """
    def __init__(self, warning: bool = None):
        self.warning = warning
