"""
Imports
"""
from typing import Dict

import eel

from report_tree.report_node import ReportNode
from report_tree.report_leaf import TextLeaf, LabelLeaf

FALLBACK_COLOUR = "#ADADAD"


def generate_tree(tree: ReportNode, tree_changes: Dict[str, str] = {}):
    """"
    Function that traverses through the given ReportNode, and uses the make_node function to create nodes and leaves
    in the right format for the UI.
    :param tree: The report node created by the NLP, containing the entire structure
    :param tree_changes: Dictionary stored in model containing all changes made on the front end,
            key: identifier, value: new label
    :return: Structured data for the front end in Json
    """
    nodes = []
    traversed_identifiers = {}

    def traverse(root: ReportNode, parent_id: str = None):
        """
        Function which traverses through tree by calling recursively calling its children,
        while calling the add_nodes function on each node.
        :param root: The node currently being traversed, containing all necessary information including children
        :param parent_id: The id of the parent of the currently traversed node, needed in the add_node function
        """
        nonlocal nodes
        new_id = create_identifier(root.category, parent_id) if parent_id else create_identifier(root.category)

        node = make_node(root, new_id, parent_id)
        if new_id in tree_changes:  # check for user change
            change_label(node, tree_changes[new_id])

        nodes.append(node)
        parent = new_id
        for child in root:
            if isinstance(child, TextLeaf):
                process_leaf(child, parent)
            else:
                traverse(child, parent)

    def process_leaf(leaf: TextLeaf, parent_id: str):
        """
        Calls the add_nodes function on the leaves and their text, adding 2 nodes
        :param leaf: The leaf currently being traversed, containing all necessary information including its text
        :param parent_id: The id of the parent of the currently traversed node, needed in the add_nodes function
        """
        nonlocal nodes
        if leaf.field != 'O':  # 'Other' leaves are currently excluded
            field_id = create_identifier(leaf.field, parent_id)
            value_id = create_identifier(leaf.text, field_id)
            field, value = make_leaf(leaf, field_id, value_id, parent_id)

            if field_id in tree_changes:  # check for user change
                change_label(field, tree_changes[field_id])
            if value_id in tree_changes:  # check for user change
                change_label(value, tree_changes[value_id])

            nodes.extend([field, value])

    def create_identifier(*args: list):
        """
        Creates a string from the input strings, used as id of a node/leaf,
        Used to link user changes to a changing tree
        :param args: Either text + label + parent_id  or  category + parent_id
        :return: A string concatenation of the input strings
        """
        nonlocal nodes, traversed_identifiers
        identifier_string = ""
        for arg in args[:-1]:
            identifier_string += str(arg) + "_"
        identifier_string += str(args[-1])

        if identifier_string not in traversed_identifiers:
            traversed_identifiers[identifier_string] = 1
        else:
            traversed_identifiers[identifier_string] += 1
            identifier_string = identifier_string + str(traversed_identifiers[identifier_string])

        return identifier_string

    traverse(tree)
    return nodes


def make_node(node: ReportNode, identifier: str, parent_id: str):
    """
    Create a regular (category) node, in json/dictionary format
    :param node: object that represents the node
    :param identifier: The id given to the node currently being added, giving this node the currently highest index
    :param parent_id: The id of the parent of the node/leaf currently being added
    """
    node = json_node_template(identifier, parent_id, node.category)

    return node


def make_leaf(leaf: TextLeaf, identifier_field: str, identifier_value: str, parent_id: str):
    """
    Create a leaf, which consists of two json objects: the leaf key and the leaf value
    :param leaf: object that represents the leave
    :param identifier_value: The id given to the label of the leaf
    :param identifier_field: The id given to the key of the leaf
    :param parent_id: The id of the parent of the leaf currently being added
    :return: a list containing the key and value json objects
    """

    # Field
    leaf_field = json_node_template(
        identifier=identifier_field,
        parent_id=parent_id,
        text=leaf.field,
        confidence=leaf.field_conf,
        hint=leaf.hint,
        speculative=leaf.speculative
    )

    # Value
    if isinstance(leaf, LabelLeaf):
        leaf_value = json_node_template(
            identifier=identifier_value,
            parent_id=identifier_field,
            text=leaf.label,
            confidence=leaf.label_conf,
            hint=leaf.text,
            alternatives={leaf.text: round(leaf.label_conf * 100), **{x: 0 for x in leaf.labels}},
            value_node=True,
            speculative=leaf.speculative
        )
    else:
        leaf_value = json_node_template(identifier_value, identifier_field, leaf.text, value_node=True)

    return leaf_field, leaf_value


def json_node_template(identifier: str, parent_id: str, text: str, confidence: float = None,
                       hint: str = None, alternatives: Dict[str, float] = None, value_node: bool = False,
                       speculative: bool = False):
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
    template_text = "?" if speculative and value_node else text
    template = "<div class=\"domStyle\"><span>{}</span></div>".format(template_text)
    low_confidence = False
    if confidence:
        percentage = round(confidence * 100)
        low_confidence = percentage < 75
        template += "<span class=\"confidence\">{}%</span>".format(percentage)  # generate confidence template

    if parent_id is not None:
        par = parent_id
    else:
        par = None

    return {
        "nodeId": identifier,
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
        "label": template_text
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


def change_label(node: dict, new_label: str):
    """
    Helper function that is called when the node is being traversed has a stored edit.
    Changes the label and the template before it is added to the list of json nodes.
    :param node: The node currently being traversed, to which an edit should be applied.
    :param new_label: The new label that should be displayed in the front-end.
    """
    node['label'] = new_label
    node[
        'template'] = "<div class=\"domStyle\"><span>" + new_label + \
                      "</div></span><span class=\"material-icons\">mode</span>"


def initialize(model):
    """
    Initialize view in frontend with initial data
    """
    eel.initialize_frontend(list(model.environments.keys()))


def update(model):
    """
    Reflect the changes to the model in the front-end
    """
    linear_tree = generate_tree(model.tree, model.tree_changes)
    visual_text = set_node_colours(model.tree, "", model.colours)
    eel.update_frontend(linear_tree, model.environment, visual_text)


def server_error(mess: str):
    """
    Method used to display an error in the connection to the server
    :param mess: The message of the server error
    # :param mess: The accompanying error message
    """
    eel.show_server_error(mess)
