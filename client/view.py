"""
Imports
"""
from typing import Dict, List

import eel

from report_tree.report_node import ReportNode
from report_tree.report_leaf import TextLeaf, LabelLeaf

FALLBACK_COLOUR = "#ADADAD"


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
        nodes.append(make_node(root, new_id, parent_id))
        parent = new_id
        new_id += 1
        for child in root:
            if isinstance(child, TextLeaf):
                process_leaf(child, parent)
            elif isinstance(child, ReportNode):
                traverse(child, parent)

    def process_leaf(leaf: TextLeaf, parent_id: int):
        """
        Calls the add_nodes function on the leaves and their text, adding 2 nodes
        :param leaf: The leaf currently being traversed, containing all necessary information including its text
        :param parent_id: The id of the parent of the currently traversed node, needed in the add_nodes function
        """
        nonlocal new_id
        if leaf.field != 'O':  # 'Other' leaves are currently excluded
            nodes.extend(make_leaf(leaf, new_id, parent_id))
            new_id += 2  # increment with 2, since leaves contain of 2 json objects

    traverse(tree)
    return nodes


def make_node(node: ReportNode, identifier: int, parent_id: int):
    """
    Create a regular (category) node, in json/dictionary format
    :param node: object that represents the node
    :param identifier: The id given to the node currently being added, giving this node the currently highest index
    :param parent_id: The id of the parent of the node/leaf currently being added
    """
    node = json_node_template(identifier, parent_id, node.category)

    return node


def make_leaf(leaf: TextLeaf, field_id: int, parent_id: int):
    """
    Create a leaf, which consists of two json objects: the leaf key and the leaf value
    :param leaf: object that represents the leave
    :param field_id: The id given to the key of the leaf, the value will have the id incremented with one
    :param parent_id: The id of the parent of the leaf currently being added
    :return: a list containing the key and value json objects
    """

    # Field
    leaf_field = json_node_template(
        identifier=field_id,
        parent_id=parent_id,
        text=leaf.field,
        confidence=leaf.field_conf,
        hint=leaf.hint,
        speculative=leaf.speculative
    )

    # Value
    value_id = field_id + 1
    if isinstance(leaf, LabelLeaf):
        leaf_value = json_node_template(
            identifier=value_id,
            parent_id=field_id,
            text=leaf.label,
            confidence=leaf.label_conf,
            hint=leaf.text,
            alternatives=list(leaf.labels),
            value_node=True,
            speculative=leaf.speculative
        )
    else:
        leaf_value = json_node_template(
            identifier=value_id,
            parent_id=field_id,
            text=leaf.text,
            value_node=True,
            speculative=leaf.speculative
        )

    return [leaf_field, leaf_value]


def json_node_template(identifier: int, parent_id: int, text: str, confidence: float = None, hint: str = None,
                       alternatives: List = None, value_node: bool = False, speculative: bool = False):
    """
    Helper function that generates a basic structure for the json objects used in functions above
    :param hint: The hint, if it is a key node
    :param identifier: the id for the json object
    :param parent_id: the id of the parent of the json object
    :param text: the text that is used in the default HTML template of the json object
    :param confidence: the confidence for the node
    :param alternatives: the alternative texts
    :param value_node: whether the node is a value.
    :param speculative: whether the node is auto-generated
    :return: a python dict representing the json object
    """
    if text is None:
        text = "?"
    template = "<div class=\"domStyle\"><span>{}</span></div>".format(text)

    low_confidence = False
    if confidence:
        percentage = round(confidence * 100)
        low_confidence = percentage < 75
        template += "<span class=\"confidence\">{}%</span>".format(percentage)  # generate confidence template

    if parent_id is not None:
        par = str(parent_id)
    else:
        par = None

    return {
        "nodeId": str(identifier),
        "parentNodeId": par,
        "valueNode": value_node,
        "lowConfidence": low_confidence,
        "width": 347,
        "height": 147,
        "template": template,
        "alternatives": alternatives,
        "originalTemplate": template,
        "hint": hint,
        "text": text,
        "speculative": speculative,
    }


def set_node_colours(node: ReportNode, parent_label: str, colours: Dict[str, str]):
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
        if isinstance(child, TextLeaf):
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


def set_leaf_colours(leaf: TextLeaf, parent_label: str, colours: Dict[str, str]):
    """
    Method used to create the text object with colour for the leaves
    :param leaf: The TextLeaf which needs to get a colour
    :param parent_label: The label of the parent
    :param colours: The colour dictionary for the current environment
    :return: Returns the object needed for the frontend
    """
    if leaf.speculative:
        return None
    label = "{}{}".format(parent_label, leaf.field)
    if leaf.field == "O":
        result_type = "other"
        colour = None
    else:
        result_type = "label"
        colour = colours.get(leaf.field, FALLBACK_COLOUR)
    return {
        "text": leaf.text,
        "colour": colour,
        "type": result_type,
        "label": label,
    }


def initialize(model):
    """
    Initialize view in frontend with initial data
    """
    eel.initialize_frontend(list(model.environments.keys()))


def update(model):
    """
    Reflect the changes to the model in the front-end
    """
    linear_tree = generate_tree(model.tree)
    visual_text = set_node_colours(model.tree, "", model.colours)
    eel.update_frontend(linear_tree, model.environment, visual_text)


def server_error(mess: str):
    """
    Method used to display an error in the connection to the server
    :param mess: The message of the server error
    # :param mess: The accompanying error message
    """
    eel.show_server_error(mess)
