"""
Presenter class
"""
import eel

from tree_changes import NodeChange, LeafChange
from model import Model
import view
from ui_automation import UIAutomation

model = Model(view.initialize, view.update, view.server_error, view.show_loader)


@eel.expose
def update_environment(new_environment):
    """
    Update the model using the new_environment
    :param new_environment: string corresponding to new environment
    """
    model.set_environment(new_environment)


@eel.expose
def update_tree(identifier, changed_type, value):
    # if changed_type == "label":
    #     model.tree_changes =
    change = model.get_or_create_change(identifier)
    change[changed_type] = value

    # """
    # Recieve tree update from front-end and update model
    # :param new_tree: the updated tree in json format
    # """
    # original_tree = view.generate_tree(model.tree, model.tree_identifiers, {})
    # tree_changes = tree_user_changes_map(new_tree, original_tree)
    # model.set_changes_map(tree_changes)


def tree_user_changes_map(new_tree, original_tree):
    """
    Generate map of changes between two trees
    :param new_tree: the new tree in json format
    :param old_tree: the old tree in json format
    :return: a dictionary mapping hashes from the old nodes to labels of new nodes
    """
    tree_changes = {}
    new_to_orig = {id(new): orig for new, orig in zip(new_tree, original_tree)}
    values = [new for new in new_tree if new['valueNode']]
    field_ids = [new['parentNodeId'] for new in values]
    fields = [field for field in new_tree if field['nodeId'] in field_ids]
    fields_to_values = {id(field): value for field, value in zip(fields, values)}
    nodes = [new for new in new_tree if new not in values and new['parentNodeId'] not in fields]

    # Check for node change
    for new_node in nodes:
        orig_node = new_to_orig[id(new_node)]
        changes_count = 0
        for new_value, orig_value in zip(new_node.values(), orig_node.values()):
            if new_value != orig_value: changes_count += 1
        if changes_count > 0:
            tree_changes[new_node['nodeId']] = NodeChange(new_node['label'], new_node['lowConfidence'])

    # Check for leaf change
    for new_field in fields:
        orig_field = new_to_orig[id(new_field)]
        new_label = fields_to_values[id(new_field)]
        orig_label = new_to_orig[id(new_label)]
        changes_count = 0
        # Check for field change
        for new_value, orig_value in zip(new_field.values(), orig_field.values()):
            if new_value != orig_value: changes_count += 1
        # Check for label change
        for new_value, orig_value in zip(new_label.values(), orig_label.values()):
            if new_value != orig_value: changes_count += 1
        if changes_count > 0:
            tree_changes[new_field['nodeId']] = LeafChange(new_field['label'], new_label['label'], new_field['lowConfidence'], new_label['lowConfidence'])

    return tree_changes


def update_text(new_text):
    """
    Update the model using the new_text
    :param new_text: The updated text
    """
    model.set_text(new_text)


def main():
    """
    Main loop of the controller
    """
    eel.init('web')
    eel.start('index.html', block=False)
    model.retrieve_initial_data()
    ui_automation = UIAutomation(update_text)
    ui_automation.start()


if __name__ == '__main__':
    main()
