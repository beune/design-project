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
        nodes.append(make_node(root, new_id, parent_id))
        parent = new_id
        new_id += 1

        for expects_label in root.expects:  # add expects nodes
            nodes.append(json_node_template(new_id, parent, expects_label))
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


def make_leaf(leaf: ReportLeaf, identifier: int, parent_id: int):
    """
    Create a leaf, which consists of two json objects: the leaf key and the leaf value
    :param leaf: object that represents the leave
    :param identifier: The id given to the key of the leaf, the value will have the id incremented with one
    :param parent_id: The id of the parent of the leaf currently being added
    :return: a list containing the key and value json objects
    """
    leaf_key = json_node_template(identifier, parent_id, leaf.field)
    if leaf.labels:
        label, conf = leaf.best_label_conf_pair  # get label, confidence pair with highest confidence
    else:
        label, conf = "other", 0
    cert = round(conf * 100)  # certainty percentage
    template = "<div class=\"domStyle\"><span>" + label + "</span></div><span class=\"confidence\">" \
               + str(cert) + "%</span>"  # generate confidence template
    leaf_value_identifier = identifier + 1
    leaf_value_parent = identifier

    leaf_value = json_node_template(leaf_value_identifier, leaf_value_parent, label, template)
    leaf_value["alternatives"] = ["{} ({}%)".format(x, round(leaf.labels[x] * 100)) for x in leaf.labels]
    leaf_value["text"] = leaf.text
    leaf_value["valueNode"] = True
    leaf_value["lowConfidence"] = conf <= 0.75  # TODO implement low confindence

    return [leaf_key, leaf_value]


def json_node_template(identifier: int, parent_id: int, label: str, template: str = None):
    """
    Helper function that generates a basic structure for the json objects used in functions above
    :param identifier: the id for the json object
    :param parent_id: the id of the parent of the json object
    :param label: the label that is used in the default HTML template of the json object
    :param template: optional argument if a modified template is to be used
    :return: a python dict representing the json object
    """
    if template is None:  # default template
        template = "<div class=\"domStyle\"><span>" + label + "</span></div>"

    if parent_id is not None:
        par = str(parent_id)
    else:
        par = None

    node = {"nodeId": str(identifier),
            "parentNodeId": par,
            "valueNode": False,
            "lowConfidence": False,
            "width": 347,
            "height": 147,
            "template": template,  # add
            "alternatives": None,
            "originalTemplate": template,
            "hint": None,
            "text": None}

    return node


def notify(model):
    """
    Reflect the changes to the model in the front-end
    """
    linear_tree = generate_tree(model.tree)
    print(linear_tree)
    eel.change_state(linear_tree, model.environment, model.text)
