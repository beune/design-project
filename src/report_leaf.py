"""
Imports
"""
from typing import Dict


class ReportLeaf:
    """
    Class used to represent Leaves
    """
    def __init__(self, label: str, values: Dict[str, float], hint: str = None):
        self.label = label
        self.values = values
        self.hint = hint

    def __repr__(self):
        return 'Leaf {}: {}'.format(self.label, self.values)

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.label == other.label \
               and self.values == other.values
