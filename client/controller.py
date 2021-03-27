"""
Presenter class
"""
import eel
from model import Model
import view

model = Model(view.initialize, view.update, view.server_error)


@eel.expose
def update_environment(new_environment):
    """
    Update the model using the new_environment
    :param new_environment: string corresponding to new environment
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
    eel.start('index.html', block=False)
    model.retrieve_initial_data()
    from client.pim import Pim
    ui_automation = Pim(update_text)
    ui_automation.start()


if __name__ == '__main__':
    main()
