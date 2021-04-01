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
def update_tree(identifier, changed_type, value):
    """
    On tree update from front end, pass changes to model
    :param identifier: the node the change was applied to
    :param changed_type: the type of change, i.e. what field needs to be updated
    :param value: the value of the change field
    """
    model.set_change(identifier, changed_type, value)


@eel.expose
def add_to_db():
    """
    Method used to store the current tree in the database
    """
    model.add_to_db()


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
