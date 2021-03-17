"""
Imports
"""
import threading
from typing import Callable

from pywinauto.application import Application
import time


class UIAutomation:
    """
    Class which retrieves the text from the G2 speech window(Notepad for now)
    """
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.app = None
        self.textfield = None
        self.text = ""

    def updateg2(self):
        """
        Updates the text to the new text in the G2 speech window (Notepad for now)
        """
        while True:
            new_text = self.textfield.window_text()
            if new_text != self.text:
                start_time = time.time()
                flag = True
                while flag:
                    new_text = self.textfield.window_text()
                    if len(new_text) > 0 and (new_text[-1] == ' ' or time.time() - start_time > 2):
                        self.text = new_text
                        print(self.text)
                        flag = False

    def stop(self):
        """
        Stops the Notepad application
        """
        self.app.kill()

    def get_text(self) -> str:
        """
        Method used to retrieve the current text from the UIAutomation
        :return: The current text
        """
        return self.text

    def start(self):
        """
        Starts the thread which continuously checks the G2 speech
        window for new text
        """
        self.app = Application().start("notepad.exe")
        self.textfield = self.app.UntitledNotepad.Edit
        update_thread = threading.Thread(target=self.updateg2)
        update_thread.start()
