"""
Imports
"""
import eel

from report_tree.report_node import ReportNode
from report_tree.report_leaf import ReportLeaf


def generate_tree(tree: ReportNode):
    """"
    Function that traverses through the given ReportNode, and uses the make_node function to create nodes and leaves
    in the right format for the UI.
    :param tree: The reportnode created by the NLP, containing the entire structure
    :return: Structured data for the front end in Json
    """
    nodes = []
    new_id = 0

    def traverse(root: ReportNode, parent_id: int = None):
        """
        Function which traverses through tree by calling recursively calling its children,
        while calling the add_nodes function on each node.
        :param root: The node currently being traversed, containing all necessary information including children
        :param parent_id: The id of the parent of the currently traversed node, needed in the add_node function
        """
        nonlocal new_id
        nodes.append(make_node(new_id, parent_id, root.category))
        parent = new_id
        new_id += 1
        for child in root:
            if isinstance(child, ReportLeaf):
                process_leaf(child, parent)
            else:
                traverse(child, parent)

    def process_leaf(leaf: ReportLeaf, parent_id: int):
        """
        Calls the add_nodes function on the leaves and their text, adding 2 nodes
        :param leaf: The leaf currently being traversed, containing all necessary information including its text
        :param parent_id: The id of the parent of the currently traversed node, needed in the add_nodes function
        """
        nonlocal new_id
        nodes.append(make_node(new_id, parent_id, leaf.field, leaf.fieldconf))
        old_id = new_id
        new_id += 1

        label, conf = leaf.best_label_conf_pair
        nodes.append(make_node(new_id, old_id, label, conf))
        new_id += 1

    traverse(tree)
    return nodes


def make_node(identifier: int, parent_id: int, label: str, prob: float = None):
    """
    Adds a node and its corresponding information to the nodes list, in json/dictionary format
    :param identifier: The id given to the node/leaf currently being added, giving this node the currently highest index
    :param parent_id: The id of the parent of the node/leaf currently being added
    :param label: The name of the node/leaf currently being added
    :param prob: certainty of the label on the leaf
    """

    if prob:
        cert = round(prob * 100)
        template = "<div class=\"domStyle\"><span>" + label + "</span></div><span class=\"confidence\">" \
                   + str(cert) + "%</span>"
    else:
        template = "<div class=\"domStyle\"><span>" + label + "</span></div>"

    node = {"nodeId": str(identifier),
            "parentNodeId": str(parent_id),
            "width": 347,
            "height": 147,
            "borderRadius": 15,
            "template": template,
            "alternatives": None,
            "label": str(label)}

    return node


def notify(model):
    """
    Reflect the changes to the model in the front-end
    """
    linear_tree = generate_tree(model.tree)
    eel.change_state(linear_tree, model.environment, model.text)
