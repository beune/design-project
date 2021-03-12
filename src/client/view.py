"""
Imports
"""
from src.client.controller import Controller
from src.report_node import ReportNode
from src.report_leaf import ReportLeaf
import json

import pprint


class IdCounter:
    """
    Class used to keep track of the node ids while creating the nodes list
    """

    def __init__(self):
        self.identifier = 0

    def increase(self):
        """
        Increases the identifier, called when a new node is created
        """
        self.identifier += 1


class Nodes:
    """"
    Class used to store the node list that's being created
    """

    def __init__(self):
        self.nodes = []

    def add_node(self, node: dict):
        """
        Adds a node and all it's information to the list of nodes
        """
        self.nodes.append(node)


def get_tree(text: str):
    """
    Sends the input text to and the gets the tree from the controller.
    :param text: The input text that is sent
    :return: A ReportNode containing the desired structure.
    """
    c = Controller()                         # TODO Establish correct connection between view and controller
    tree = c.get_parsed_text_temp("", "")    # fixme controller weet dondersgoed wat er staat in environment en de text
    return tree


def traverse(root: ReportNode, id_count: IdCounter, nodes: Nodes, parent_id: int = None):
    """
    Function which traverses through tree by calling recursively calling its children,
    while calling the add_nodes function on each node.
    :param root: The node currently being traversed, containing all necessary information including children
    :param id_count: The class containing the id of the previously traversed node
    :param nodes: Class containing the list of nodes, needed for the add_node function
    :param parent_id: The id of the parent of the currently traversed node, needed in the add_node function
    """
    identifier = id_count.identifier
    add_node(identifier, parent_id, root.label, nodes)
    id_count.increase()
    for child in root:
        if isinstance(child, ReportLeaf):
            process_leaf(child, identifier, id_count, nodes)
        else:
            traverse(child, id_count, nodes, identifier)


def process_leaf(leaf: ReportLeaf, parent_id: int, id_count: IdCounter, nodes: Nodes):
    """
    Calls the add_nodes function on the leaves and their text, adding 2 nodes
    :param leaf: The leaf currently being traversed, containing all necessary information including its text
    :param parent_id: The id of the parent of the currently traversed node, needed in the add_nodes function
    :param id_count: The class containing the id of the previously traversed node, used to set new id's
    :param nodes: Class containing the list of nodes, needed for the add_node function
    """
    identifier_node = id_count.identifier
    add_node(identifier_node, parent_id, leaf.label, nodes)
    id_count.increase()

    identifier_leaf = id_count.identifier
    add_node(identifier_leaf, identifier_node, leaf.text, nodes)
    id_count.increase()


def add_node(identifier: int, parent_id: int, label: str, nodes: Nodes):
    """
    Adds a node and its corresponding information to the nodes list, in json/dictionary format
    :param identifier: The id given to the node/leaf currently being added, giving this node the currently highest index
    :param parent_id: The id of the parent of the node/leaf currently being added
    :param label: The name of the node/leaf currently being added
    :param nodes: The class containing the list of nodes, destination of this node
    """
    template = "<div class=\"domStyle\"><span>" + label + "</span></div>"

    node = {"nodeId": str(identifier),
            "parentNodeId": str(parent_id),
            "template": template,
            "alternatives": None,
            "label": str(label)}
    nodes.add_node(node)


def send_to_front(nodez: Nodes):
    """
    Sends the desired json structure to the UI
    """
    # TODO: This is a temporary
    with open('Place your file here folks', 'w') as outfile:
        json.dump(nodez.nodes, outfile)


if __name__ == "__main__":
    test_tree = get_tree("cheese")
    test_nodes = Nodes()
    test_id_counter = IdCounter()
    traverse(test_tree, test_id_counter, test_nodes)
    print(test_nodes.nodes)
    pprint.PrettyPrinter().pprint(test_nodes.nodes)
