import tkinter as tk

class MenuRibbon:
    def __init__(self, root):
        self.root = root
        self.ribbon = tk.Menu(self.root)
        self.root.config(menu=self.ribbon)
        self.file_menu = tk.Menu(self.ribbon)
        self.file_menu.add_command(label="Opslaan")
        self.view_menu = tk.Menu(self.ribbon)
        self.view_menu.add_command(label="Boom view")
        self.view_menu.add_command(label="File view")
        help_menu = tk.Menu(self.ribbon)
        help_menu.add_command(label="Help pwease :(")

        self.ribbon.add_cascade(label="Bestand", menu=self.file_menu)
        self.ribbon.add_cascade(label="Beeld", menu=self.view_menu)
        self.ribbon.add_cascade(label="Help", menu=help_menu)
