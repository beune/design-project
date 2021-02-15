import atexit
import time
from threading import Thread

from pywinauto.application import Application

class UIAutomation:

    def __init__(self):
        self.app = Application().start("notepad.exe")
        self.textwindow = self.app.UntitledNotepad.Edit
        self.text = ""

    def update(self):
        while True:
            newtext = self.textwindow.window_text()
            if newtext != self.text:
                starttime = time.time()
                flag = True
                while flag:
                    newtext = self.textwindow.window_text()
                    if len(newtext) > 0 and (newtext[-1] == ' ' or time.time() - starttime > 2):
                        self.text = newtext
                        print(self.text)
                        flag = False

    # def check_for_words

    def stop(self):
        self.app.kill()

    def start(self):
        update_thread = Thread(target=self.update)
        update_thread.start()

if __name__ == "__main__":
    x = UIAutomation()
    x.start()
    atexit.register(x.stop)

