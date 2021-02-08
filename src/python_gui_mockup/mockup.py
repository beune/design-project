#!/usr/bin/env python3
# github.com/Akuli/tkinter-tutorial
# TODO dependency:
# pacman: tk package

import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()

row = 1

def quit():
    if messagebox.askyesno("Afsluiten", "Wilt u echt het programma afsluiten?"):
        root.destroy()

def toggle():
    global row
    ttk.Entry(values_frame).grid(row=row, column=0, sticky="NEW", pady=2, padx=2)
    ttk.Entry(values_frame).grid(row=row, column=1, sticky="NEW", pady=2, padx=2)
    row += 1

content = ttk.Frame(root, padding=(3,3,3,3))
text_frame = ttk.Frame(content, borderwidth=5, relief="ridge")
# TODO text starts vertically in the middle and does not wrap
text_entry = ttk.Entry(text_frame)
values_frame = ttk.Frame(content, borderwidth=5)

start_stop_button = ttk.Button(content, text="Start/stop", command=toggle)

content.grid(column=0, row=0, sticky=("NSEW"))
text_frame.grid(column=0, row=0, columnspan=3, rowspan=4, sticky=("NSEW"))
text_entry.grid(column=0, row=0, sticky="NSEW")
values_frame.grid(column=3, row=0, columnspan=1, sticky=("NSEW"))
start_stop_button.grid(column=3, row=3, sticky=("EW"))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

text_frame.columnconfigure(0, weight=1)
text_frame.rowconfigure(0, weight=1)

values_frame.columnconfigure(0, weight=1)
values_frame.columnconfigure(1, weight=1)

content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=3)
content.rowconfigure(1, weight=1)

if __name__ == "__main__":
    # root.protocol('WM_DELETE_WINDOW', quit)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        exit()
