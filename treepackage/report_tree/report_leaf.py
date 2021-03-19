"""
Imports
"""
from typing import Dict, Tuple


class ReportLeaf:
    """
    Class used to represent Leaves
    """
    def __init__(self, text: str, field: str, fieldconf: float, labels: Dict[str, float] = None, hint: str = None):
        self.text = text
        self.field = fiel
        self.fieldconf = fieldconf
        self.labels = labels if labels else {}
        self.hint = hint

    def __repr__(self):
        return 'Leaf {}: {} {}'.format(self.key, self.text, self.labels.keys())

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.text == other.text \
               and self.key == other.key \
               and self.conf == other.conf \
               and self.labels == other.labels

    @property
    def best_label_conf_pair(self) -> Tuple[str, float]:
        """
        Return the label with the highest confidence and the corresponding confidence
        :return:
        """
        value = max(self.labels, key=self.labels.get)
        return value, self.labels[value]
