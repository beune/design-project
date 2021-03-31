class NodeChange:
    def __init__(self, category: str, warning: bool):
        self.category = category
        self.warning = warning


class LeafChange:
    def __init__(self, field: str, label: str, field_warning: bool, label_warning: bool, deleted: bool):
        self.field = field
        self.label = label
        self.field_warning = field_warning
        self.label_warning = label_warning
        self.deleted = deleted


class Change:
    def __init__(self, label: str = None, warning: bool = None, deleted: bool = None):
        self.label = label
        self.warning = warning
        self.deleted = deleted
