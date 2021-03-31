"""
Presenter class
"""
import eel
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
def update_tree(new_tree):
    """
    Recieve tree update from front-end and update model
    :param new_tree: the updated tree in json format
    """
    old_tree = view.generate_tree(model.tree, model.tree_changes)
    tree_changes = tree_user_changes_map(new_tree, old_tree)
    model.set_changes_map(tree_changes)
    model.set_tree_edited(view.tree_from_json(new_tree, new_tree[0]))


def tree_user_changes_map(new_tree, old_tree):
    """
    Generate map of changes between two trees
    :param new_tree: the new tree in json format
    :param old_tree: the old tree in json format
    :return: a dictionary mapping hashes from the old nodes to labels of new nodes
    """
    tree_changes = {}
    for new_node, old_node in zip(new_tree, old_tree):
        if new_node['label'] != old_node['label'] or new_node['lowConfidence'] != old_node['lowConfidence']:
            tree_changes[old_node['nodeId']] = new_node
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
