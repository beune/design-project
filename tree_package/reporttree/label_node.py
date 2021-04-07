from typing import List, Tuple
from reporttree.node import Node


class LabelNode(Node):
    def __init__(self, path: List[str], options: List[str], text_prediction: Tuple[str, int] = (None, None),
                 label_prediction: Tuple[str, int] = (None, None), children: List['Node'] = None, hint: str = None):
        """
        Constructor for Nodes that can be labeled
        :param category: The category of the LabelNode
        :param labels: Ordered list of possible labels
        :param text_prediction: The text the NLP predicts to have this category with the confidence
        :param predicted_label: The label the NLP predicts based on the text with the confidence
        :param children: The children of this Node
        :param hint: Hint for this Node
        """
        super().__init__(path, text_prediction, children, hint)
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

    def is_corrected(self) -> bool:
        """
        Whether the text or label is corrected
        :return: True if corr_text or corr_label is set
        """
        return super().is_corrected() or self.corr_label is not None

    @property
    def label(self) -> str:
        """
        The label of the node
        :return: corr_label if set, otherwise pred_label
        """
        if self.corr_label:
            return self.corr_label
        return self.pred_label
