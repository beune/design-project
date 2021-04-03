"""
Imports
"""
from typing import Dict

import eel
from client_package.model import Model
from reporttree.node import Node
from reporttree.label_node import LabelNode
from client_package.tree_changes import FrontChange

FALLBACK_COLOUR = "#ADADAD"


def generate_tree(model: Model) -> list:
    """"
    Function that traverses through the given ReportNode, and uses the make_node function to create nodes and leaves
    in the right format for the UI.
    :param model The model of our application
    :return: Structured data for the front end in Json
    """
    nodes = []

    def traverse(node: Node, parent_id: str = None):
        """
        Function which traverses through tree by calling recursively calling its children,
        while calling the add_nodes function on each node.
        :param node: The node currently being traversed, containing all necessary information including children
        :param parent_id: The id of the parent of the currently traversed node, needed in the add_node function
        """
        nonlocal nodes

        identifier = model.tree_identifiers[id(node)]
        change = model.front_changes.get(identifier)
        leafchange = model.front_changes.get(identifier + "_value")
        nodes += make_node(node, identifier, parent_id, change, leafchange)
        for child in node:
            if child.category != "O":
                traverse(child, identifier)

    traverse(model.tree)
    return nodes


def make_node(node: Node, identifier: str, parent_id: str, change: FrontChange, leaf_change: FrontChange) -> list:
    """
    Method used to create a jsontemplate from a node
    :param leaf_change: Possible change to the actual leaf if the node is a leaf
    :param node: The node that needs to be converted into a json representation
    :param identifier: The identifier of the node
    :param parent_id: The id of the parent of the node
    :param change: possible change accompanied with the node
    :return: list of json representations of the node
    """
    tmp = json_node_template(node, identifier, parent_id, change, False)
    if node.is_leaf():
        field = json_node_template(node, identifier + "_value", identifier, leaf_change, True)
        return [tmp, field]
    return [tmp]


def json_node_template(node: Node, identifier: str, parent_id: str, change: FrontChange, leaf: bool):
    """
    Method used to create a json template of any node in the tree
    :param node: The node for which
    :param identifier:
    :param parent_id:
    :param change:
    :param leaf:
    :return:
    """
    hint = None
    alternatives = None
    low_confidence = False
    percentage = None
    if leaf:
        if isinstance(node, LabelNode):
            text = node.label
            alternatives = node.options
            percentage = node.pred_label_conf
        else:
            text = node.text
            percentage = node.pred_text_conf
        hint = node.text
    else:
        percentage = node.pred_text_conf
        text = node.category
        hint = node.hint

    if not text:
        text = "?"
    template = "<div class=\"domStyle\"><span>{}</span></div>".format(text)

    if percentage:
        low_confidence = percentage < 75
        template += "<span class=\"confidence\">{}%</span>".format(percentage)  # generate confidence template

    if leaf:
        if node.is_speculative():
            background_color = "#E6BEBC"
            outline_color = "#E6BEBC"
            text_color = "#FFFFFF"
        else:
            background_color = "#EF7104"
            outline_color = "#EF7104"
            text_color = "#FFFFFF"

    else:
        if node.is_speculative():
            background_color = "#ADCBF8"
            outline_color = "#ADCBF8"
            text_color = "#FFFFFF"

        else:
            background_color = "#5A9AFA"
            outline_color = "#5A9AFA"
            text_color = "#FFFFFF"

    jsonnode = {
        "nodeId": identifier,
        "parentNodeId": parent_id,
        "lowConfidence": low_confidence,
        "width": 347,
        "height": 147,
        "template": template,
        "alternatives": alternatives,
        "hint": hint,
        "text": text,
        "speculative": node.is_speculative(),
        "backgroundColor": background_color,
        "textColor": text_color,
        "outlineColor": outline_color,
        "leaf": leaf,
    }

    if change:
        apply_change(jsonnode, change)
    return jsonnode


def set_node_colours(node: Node, parent_label: str, colours: Dict[str, str]):
    """
    Method used to create the text object with colour for nodes
    :param node: The ReportNode which needs to be formed into the right format for the frontend
    :param parent_label: The label of the parent of the node
    :param colours: The colourdictionary for the current environment
    :return: Returns the object generated out the node for the frontend
    """
    children = []
    label = parent_label + node.category
    for child in node:
        if child.is_leaf():
            res = set_leaf_colours(child, label + "/", colours)
        else:
            res = set_node_colours(child, label + "/", colours)
        if res:
            children.append(res)
    if children:
        return {
            "children": children,
            "type": "node",
            "label": label,
        }
    else:
        return None


def set_leaf_colours(node: Node, parent_label: str, colours: Dict[str, str]):
    """
    Method used to create the text object with colour for the leaves
    :param node: The TextLeaf which needs to get a colour
    :param parent_label: The label of the parent
    :param colours: The colour dictionary for the current environment
    :return: Returns the object needed for the frontend
    """

    if node.is_speculative():
        return None
    label = parent_label + node.category
    if node.is_leaf():
        if node.category == "O":
            result_type = "other"
            colour = None
        else:
            label = label + "/" + node.category
            result_type = "label"
            colour = colours.get(node.category, FALLBACK_COLOUR)
    else:
        result_type = "label"
        colour = colours.get(node.category, FALLBACK_COLOUR)
    return {
        "text": node.text,
        "colour": colour,
        "type": result_type,
        "label": label,
    }


def apply_change(node, change: FrontChange):
    """
    Given json node (to be sent to front end), apply changes to it
    :param node: the json node (actually python dict) to which change should be applied
    :param change: the Change object, containing fields that should be altered in json node
    """
    node['lowConfidence'] = change.warning


def initialize(model):
    """
    Initialize view in frontend with initial data
    """
    eel.initialize_frontend(list(model.environments.keys()))


def update(model):
    """
    Reflect the changes to the model in the front-end
    """
    linear_tree = generate_tree(model)
    visual_text = set_node_colours(model.tree, "", model.colours)
    eel.update_frontend(linear_tree, model.environment, visual_text)


def show_loader(show: bool):
    """
    Method used to give visual feedback on when the NLP of the environment is loading
    :param show: Whether to show the loader or not
    """
    eel.show_loader(show)


def server_error(mess: str):
    """
    Method used to display an error in the connection to the server
    :param mess: The message of the server error
    # :param mess: The accompanying error message
    """
    eel.show_server_error(mess)


def get_tree_text(model):
    """
    Create a textual representation of the tree
    :param model: The model containing the current tree and the changes
    :return: A structured report
    """

    def traverse(node, indentations: int = 0) -> str:
        """
        Method used to traverse the tree to create the tree text
        :param node: Node that needs to be processed
        :param indentations: Current level of indentation
        :return: Textual representation of node
        """
        indentation = "\t" * indentations
        if node.is_leaf():
            if node.category == "O":
                return ""
            if isinstance(node, LabelNode):
                return indentation + str(node.category) + ": " + str(node.label) + "\n"
            else:
                return indentation + str(node.category) + ": " + str(node.text) + "\n"
        else:
            child_text = "".join(traverse(child, indentations + 1) for child in node)
            return indentation + str(node.category) + ":\n" + child_text

    return "Environment: {}\n\n{}".format(model.environment, "".join(traverse(node) for node in model.tree))
