"""
Presenter class
"""
import eel
from model import Model
import view
from ui_automation import UIAutomation

model = Model(view.initialize, view.update)


@eel.expose
def update_environment(new_environment):
    """
    Update the model using the new_environment
    :param new_environment: string corresponding to new environment
    """
    model.set_environment(new_environment)


@eel.expose
def update_tree(new_tree):
    old_tree = view.generate_tree(model.tree)
    tree_changes = tree_user_changes_map(new_tree, old_tree)
    model.set_changes_map(tree_changes)


def tree_user_changes_map(new_tree, old_tree):
    tree_changes = {}
    for new_node, old_node in zip(new_tree, old_tree):
        if new_node['label'] != old_node['label']:
            tree_changes[old_node['nodeId']] = new_node['label']
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
