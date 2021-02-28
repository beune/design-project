import tkinter as tk

class TitleBar:
    def __init__(self, root):
        self.root = root

        self.title_bar = tk.Frame(self.root, relief=tk.RAISED)
        self.title_bar.pack(side=tk.TOP, fill="x")
        self.title = tk.Label(self.title_bar, text="Mammo")
        self.title.pack(side=tk.LEFT)
