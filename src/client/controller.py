"""
Presenter class
"""
import eel
from model import Model
import view
from ui_automation import UIAutomation

model = Model(view.notify)


@eel.expose
def update_environment(new_environment) -> None:
    """
    Update the model using the new_environment
    :param new_environment:
    """
    model.set_environment(new_environment)


def update_text(new_text) -> None:
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
    ui_automation = UIAutomation(update_text)
    ui_automation.start()


if __name__ == '__main__':
    main()
