import atexit
import time
from threading import Thread

from pywinauto.application import Application

from queuespeech import QueueSpeech


class UIAutomation:

    def __init__(self, queuespeech):
        self.app = Application().start("notepad.exe")
        self.textwindow = self.app.UntitledNotepad.Edit
        self.text = ""
        self.queuespeech = queuespeech

    def update(self):
        for i in range(0,100):
            self.textwindow.set_text(self.queuespeech.text)
            time.sleep(1)
    # def check_for_words

    def stop(self):
        self.app.kill()

    def start(self):
        update_thread = Thread(target=self.update)
        update_thread.start()

if __name__ == "__main__":
    y = QueueSpeech()
    y.startup()
    x = UIAutomation(y)
    x.start()
    atexit.register(x.stop)

