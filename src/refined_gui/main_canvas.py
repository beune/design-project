import tkinter as tk


class MainCanvas:
    def __init__(self, root):
        self.root = root
        self.main_canvas = tk.Canvas(self.root, bg="white",
                                     highlightthickness=0)  # make main canvas in which to display tree
        self.main_canvas.pack(expand=1, fill="both")

        rect = self.main_canvas.create_rectangle(50, 50, 100, 100, outline='orange')

        self.main_canvas.update()
