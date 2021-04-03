from typing import List, Tuple

class Node:
    def __init__(self, category: str, text_prediction: Tuple[str, int] = (None, None), children: List['Node'] = None,
                 hint: str = None):
        self.category = category

        self.pred_text, self.pred_text_conf = text_prediction
        self.corr_text: str = None
        self.var: int = None
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
        self.children.append(child)

    def is_leaf(self):
        return not self.children

    def is_speculative(self):
        return self.text == None

    def is_corrected(self):
        return self.corr_text is not None

    # def recursive(self, call):
    #     for child in self:
    #         child.recursive(call)
    #     call(self)

    @property
    def text(self) -> str:
        if self.corr_text:
            return self.corr_text
        return self.pred_text
