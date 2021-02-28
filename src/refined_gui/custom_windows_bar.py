import tkinter as tk
import tkinter.ttk


class CustomTitleBar:
    def __init__(self, root):
        self.root = root

        self.title_bar = tk.Frame(root, relief=tk.SUNKEN, bd=0)  # make custom title bar
        self.title_bar.pack(expand=0, fill="x")  # pack in main window
        # label1 = tk.Label(self.title_bar, text="Radio", fg="black", font="Times")  # make text label for title bar
        # label1.pack(side=tk.LEFT)  # pack in title bar

        # close_button_style = tk.ttk.Style()
        # close_button_style.configure('W.TButton', font=('Segoe', 10), relief='flat', bg='red')
        self.close_button_frame = tk.Frame(self.title_bar, width=47, height=28)
        self.close_button_frame.pack(side=tk.RIGHT)  # pack in title bar
        self.close_button = tk.Button(self.close_button_frame, text="X", relief='flat', bg='red',
                                      command=root.destroy)  # make close button for title bar
        self.close_button.bind('<Enter>', self.close_button_enter)
        self.close_button.bind('<Leave>', self.close_button_leave)
        self.close_button.pack(expand=True, fill=tk.BOTH)  # pack in frame

        # top_button_style = tk.ttk.Style()
        # top_button_style.configure('TopButton', font=('Segoe', 10), background='red')
        self.minimise_button = tk.ttk.Button(self.title_bar, text="-", style='W.TButton',
                                             command=self.hide_screen)  # make minimise button for title bar
        self.minimise_button.pack(side=tk.RIGHT)  # pack in title bar

    def hide_screen(self):
        self.root.overrideredirect(0)
        self.root.iconify()

    def close_button_enter(self, e):
        e.widget['bg'] = 'blue'

    def close_button_leave(self, e):
        e.widget['bg'] = 'red'
