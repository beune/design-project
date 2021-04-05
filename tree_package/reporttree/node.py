from typing import List, Tuple


class Node:
    def __init__(self, category: str, text_prediction: Tuple[str, int] = (None, None), children: List['Node'] = None,
                 hint: str = None):
        """
        Constructor for LabelNode
        :param category: The category of the Node
        :param labels: Ordered list of possible labels
        :param text_prediction: The text the NLP predicts to have this category with the confidence
        :param children: The children of this Node
        :param hint: Hint for this Node
        """
        self.category = category

        self.pred_text, self.pred_text_conf = text_prediction
        self.corr_text: str = None
        self.children = [] if children is None else children

        self.hint = hint

    def __iter__(self):
        for child in self.children:
            yield child

    def __eq__(self, other):
        return type(self) == type(other) \
               and self.category == other.category \
               and self.text == other.text \
               and self.children == other.children

    def add_child(self, child: 'Node'):
        """
        Add a child to this Node
        """
        self.children.append(child)

    def is_leaf(self) -> bool:
        """
        Whether the Node has children
        :return: True if it has no children
        """
        return not self.children

    def is_speculative(self) -> bool:
        """
        Whether the Node is expected but not yet recognised in the text
        :return: True if no text is set
        """
        return self.text is None

    def is_corrected(self) -> bool:
        """
        Whether the text or label is corrected
        :return: True if corr_text is set
        """
        return self.corr_text is not None

    @property
    def text(self) -> str:
        """
        The text of the node
        :return: corr_text if set, otherwise pred_text
        """
        if self.corr_text:
            return self.corr_text
        return self.pred_text
