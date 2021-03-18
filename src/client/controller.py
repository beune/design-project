"""
Presenter class
"""
import eel
from model import Model
import view
from ui_automation import UIAutomation

model = Model(view.notify)


@eel.expose
def update_environment(new_environment):
    """
    Update the model using the new_environment
    :param new_environment:
    """
    model.set_environment(new_environment)


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
    # ui_automation = UIAutomation(update_text)
    # eel.spawn(ui_automation.start)
    eel.start('index.html', size=(600, 400))


if __name__ == '__main__':
    main()
