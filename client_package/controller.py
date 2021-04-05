"""
Presenter class
"""
import eel
from model import Model
import view
from ui_automation import UIAutomation

model = Model(view)
ui_automation = UIAutomation(model.set_text)


@eel.expose
def update_environment(new_environment):
    """
    Update the model using the new_environment
    :param new_environment: string corresponding to new environment
    """
    model.set_environment(new_environment)


@eel.expose
def set_change(identifier: str, change: str, value):
    """
    Apply a user change to the model
    :param identifier: the identifier of the node
    :param change: the changed attribute
    :param value: the desired value
    """
    model.change(identifier, change, value)
    view.update(model)


@eel.expose
def reset_node(identifier: str):
    """
    Reset all changes applied to a node
    :param identifier: the identifier of the node
    """
    model.reset_node(identifier)
    view.update(model)


@eel.expose
def add_to_db():
    """
    Method used to store the current tree in the database
    """
    model.add_to_db()


@eel.expose
def copy_tree():
    """
    Method used to copy the textual tree representation into notepad/G2Speech
    """
    tree_text = view.get_tree_text(model)
    ui_automation.write_tree_text(tree_text)


def main():
    """
    Start the app and ui_automation and connect to the server.
    """
    eel.init('web')
    eel.start('index.html', block=False)
    model.retrieve_initial_data()
    ui_automation.start()


if __name__ == '__main__':
    main()
