"""
Special class for pim
"""
from typing import Callable

import pyinotify


class Pim:
    """
    Class which retrieves the text from the G2 speech window(Notepad for now)
    """

    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.file = "/tmp/birad"

    def start(self):
        """
        Starts the thread which continuously checks the G2 speech
        window for new text
        """
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, self.ModHandler())
        wm.add_watch(self.file, pyinotify.IN_CLOSE_WRITE)
        notifier.loop()

    class ModHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, evt):
            with open(self.file, "r") as f:
                text = f.read()
                self.callback(text)
