"""
Imports
"""
from src.client.controller import Controller
from src.report_node import ReportNode
from src.report_leaf import ReportLeaf
import json

import pprint


def get_tree(text: str):
    """
    Sends the input text to and the gets the tree from the controller.
    :param text: The input text that is sent
    :return: A ReportNode containing the desired structure.
    """
    c = Controller()                         # TODO Establish correct connection between view and controller
    tree = c.get_parsed_text_temp("", "")
    return tree


def get_tree2(tree: ReportNode):
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

        for expects_label in root.expects:  # add expects nodes
            nodes.append(make_node(new_id, parent_id, expects_label))
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
        nodes.append(make_node(new_id, parent_id, leaf.key))
        old_id = new_id
        new_id += 1

        if leaf.key != 'O':
            label, conf = leaf.best_label_conf_pair
            nodes.append(make_node(new_id, old_id, label, leaf.text, conf))
            new_id += 1

    traverse(tree)
    return nodes


def make_node(identifier: int, parent_id: int, label: str, text: str = None, prob: float = None):
    """
    Adds a node and its corresponding information to the nodes list, in json/dictionary format
    :param text: The input plain text that resulted in this label
    :param identifier: The id given to the node/leaf currently being added, giving this node the currently highest index
    :param parent_id: The id of the parent of the node/leaf currently being added
    :param label: The name of the node/leaf currently being added
    :param prob: certainty of the label on the leaf
    """

    if prob:
        cert = round(prob * 100)
        original_template = "<div class=\"domStyle\"><span>" + label + "</span></div><span class=\"confidence\">" \
                   + str(cert) + "%</span>"
    else:
        original_template = "<div class=\"domStyle\"><span>" + label + "</span></div>"

    node = {"nodeId": str(identifier),
            "parentNodeId": str(parent_id),
            "width": 347,
            "height": 147,
            "borderRadius": 15,
            "template": original_template,              # add
            "alternatives": None,
            "originalTemplate": original_template,
            "hintTemplate": None,
            "text": text}

    return node


def send_to_front(nodes: list):
    """
    Sends the desired json structure to the UI
    """
    # TODO: This is a temporary
    with open('Place your file here folks', 'w') as outfile:
        json.dump(list, outfile)

    return list


if __name__ == "__main__":
    test_tree = get_tree("cheese")
    json_file = get_tree2(test_tree)
    print(json_file)
    pprint.PrettyPrinter().pprint(json_file)
