"""
Imports
"""
from typing import Set, Tuple


class TextLeaf:
    """
    Class used to represent Leaves
    """
    def __init__(self, field: str, field_conf: float = 0, text: str = None, hint: str = None):
        self.field = field
        self.field_conf = field_conf
        self.text = text
        self.hint = hint
        self.speculative = text is None

    def __repr__(self):
        value = "?" if self.text is None else self.text
        return 'Leaf {}: {}'.format(self.field, value)

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.text == other.text \
               and self.field == other.field \
               and self.field_conf == other.field_conf


class LabelLeaf(TextLeaf):
    """
    Class used to represent Leaves with predefined labels
    """
    def __init__(self, field: str, labels: Set[str], field_conf: float = 0, text: str = None,
                 label_pair: Tuple[str, float] = (None, 0), hint: str = None):
        super().__init__(field, field_conf, text, hint)
        self.labels = labels
        self.label, self.label_conf = label_pair

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.text == other.text \
               and self.field == other.field \
               and self.field_conf == other.field_conf \
               and self.labels == other.labels \
               and self.label == other.label \
               and self.label_conf == other.label_conf

    @property
    def best_label_conf_pair(self) -> Tuple[str, float]:
        """
        Return the label with the highest confidence and the corresponding confidence
        :return:
        """
        return self.label, self.label_conf
