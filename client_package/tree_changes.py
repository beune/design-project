"""
Classes used for user changes to the tree
"""


class BackChange:
    """
    Class used to store a user change and apply it to the tree
    """
    def __init__(self, label: str):
        self.label = label


class FrontChange:
    """
    Class used to store a change only relevant to the frontend
    """
    def __init__(self, text_warning: bool, label_warning: bool):
        self.pred_text_warning = text_warning
        self.pred_label_warning = label_warning
