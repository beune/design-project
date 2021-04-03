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
def set_back_change(identifier: str, new_label: str):
    """
    Method used to set a change relevant for the tree state
    :param identifier: Identifier of the node that needs a changed label
    :param new_label: The new label of the chosen node
    """
    model.set_back_change(identifier, new_label)


@eel.expose
def set_front_change(identifier, warning):
    """
    On tree update from front end, pass changes to model
    :param identifier: the node the change was applied to
    :param warning: Whether the warning of the node needs to be on or off
    """
    model.set_front_change(identifier, warning)


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
    print(tree_text)
    ui_automation.write_tree_text(tree_text)


def main():
    """
    Main loop of the controller
    """
    eel.init('web')
    eel.start('index.html', block=False)
    model.retrieve_initial_data()
    ui_automation.start()


if __name__ == '__main__':
    main()
