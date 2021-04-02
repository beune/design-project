class Change:
    """
    Class used to store a user change and apply it to the tree
    """
    def __init__(self, label: str = None, warning: bool = None):
        self.label = label
        self.warning = warning
