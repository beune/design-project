#!/usr/bin/env python3
# github.com/Akuli/tkinter-tutorial
# TODO dependency:
# pacman: tk package

import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

radioVar = tk.IntVar()
radioVar.set(0)

def radio():
    choice  = radioVar.get()
    if choice == 0:
       tree_view_frame.grid()
       file_view_frame.grid_remove()

    elif choice == 1:
       tree_view_frame.grid_remove()
       file_view_frame.grid()
    else:
        # TODO
        pass

def quit():
    if messagebox.askyesno("Afsluiten", "Wilt u echt het programma afsluiten?"):
        root.destroy()

content = ttk.Frame(root, padding=(10,10,10,10))
text_frame = ttk.Frame(content, borderwidth=5, relief="ridge")
results_frame = ttk.Frame(content, borderwidth=5, relief="ridge")
# TODO text starts vertically in the middle and does not wrap
text_entry = ttk.Entry(text_frame).grid(column=0, row=0, sticky="NSEW")
start_stop_button = ttk.Button(content, text="Start/stop").grid(column=0, row=1, sticky="NSEW")

results_frame.grid(column=1, row=0, rowspan=2, sticky=("NSEW"))
results_frame.columnconfigure(0, weight=1)
results_frame.columnconfigure(1, weight=1)
results_frame.rowconfigure(1, weight=1)

content.grid(column=0, row=0, sticky=("NSEW"))
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)

# To make the text entry full-size
text_frame.grid(column=0, row=0, sticky=("NSEW"))
text_frame.columnconfigure(0, weight=1)
text_frame.rowconfigure(0, weight=1)

tk.Radiobutton(results_frame, text="Tree View", variable=radioVar, value=0, command=radio).grid(column=0, row=0)
tk.Radiobutton(results_frame, text="File View", variable=radioVar, value=1, command=radio).grid(column=1, row=0)

tree_view_frame = ttk.Frame(results_frame)
tree_view_frame.grid(column=0, row=1, columnspan=2, sticky="NSEW")
tree_view_frame.columnconfigure(0, weight=1)
tree_view_frame.rowconfigure(0, weight=1)
tree_view_label = ttk.Label(tree_view_frame, text="Tree").grid(column=0, row=0, sticky="NSEW")

file_view_frame = ttk.Frame(results_frame)
file_view_frame.grid(column=0, row=1, columnspan=2, sticky="NSEW")
file_view_frame.columnconfigure(0, weight=1)
file_view_frame.rowconfigure(0, weight=1)
file_view_label = ttk.Label(file_view_frame, text="File").grid(column=0, row=0, sticky="NSEW")


if __name__ == "__main__":
    root.protocol('WM_DELETE_WINDOW', quit)
    try:
        radio()
        root.mainloop()
    except (KeyboardInterrupt, tk.TclError):
        exit()
