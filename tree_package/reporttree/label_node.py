from typing import List, Tuple
from reporttree.node import Node


class LabelNode(Node):
    def __init__(self, category: str, options: List[str], text_prediction: Tuple[str, int] = (None, None),
                 label_prediction: Tuple[str, int] = (None, None), children: List['Node'] = None, hint: str = None):
        """
        Constructor for LabelNode
        :param category: The category of the Node
        :param labels: List of possible labels
        :param text_prediction:
        :param predicted_label:
        :param children:
        :param hint:
        """
        super().__init__(category, text_prediction, children, hint)
        self.pred_label, self.pred_label_conf = label_prediction
        self.corr_label: str = None
        self.options = options

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.category == other.category \
               and self.options == other.options \
               and self.text == other.text \
               and self.label == other.label \
               and self.children == other.children

    @property
    def label(self):
        if self.corr_label:
            return corr_label
        return self.pred_label
