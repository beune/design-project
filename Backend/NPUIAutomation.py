from threading import Thread
from pywinauto.application import Application
import atexit
import time


class NPUIAutomation:

    def __init__(self):
        self.app = Application().start("notepad.exe")
        self.textfield = self.app.UntitledNotepad.Edit
        self.text = ""

    def updateg2(self):
        while True:
            new_text = self.textfield.window_text()
            if new_text != self.g2speech:
                start_time = time.time()
                flag = True
                while flag:
                    new_text = self.textfield.window_text()
                    if len(new_text) > 0 and (new_text[-1] == ' ' or time.time() - start_time > 2):
                        self.g2speech = new_text
                        print(self.g2speech)
                        flag = False

    def stop(self):
        self.app.kill()

    def start(self):
        update_thread = Thread(target=self.updateg2)
        update_thread.start()
