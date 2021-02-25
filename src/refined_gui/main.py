import tkinter as tk
import sys
import os

"""Main window"""
root = tk.Tk()  # create main window
root.minsize(int(root.winfo_screenwidth() / 2), root.winfo_screenheight())  # set size of window
root.overrideredirect(1)  # remove title bar of window


def hide_screen():
    root.overrideredirect(0)
    root.iconify()


"""Custom title bar"""
title_bar = tk.Frame(root, relief=tk.SUNKEN, bd=0)  # make custom title bar
title_bar.pack(expand=0, fill="x")  # pack in main window
label1 = tk.Label(title_bar, text="Radio", fg="black", font="Times")  # make text label for title bar
label1.pack(side=tk.LEFT)  # pack in title bar
close_button = tk.Button(title_bar, text="X", bg="grey", highlightbackground="white",
                         command=root.destroy)  # make close button for title bar
close_button.pack(side=tk.RIGHT)  # pack in title bar
minimise_button = tk.Button(title_bar, text="-", bg="grey", highlightbackground="white",
                            command=hide_screen)  # make minimise button for title bar
minimise_button.pack(side=tk.RIGHT)  # pack in title bar
main_canvas = tk.Canvas(root, bg="blue", highlightthickness=0)  # make main canvas in which to display tree
main_canvas.pack(expand=1, fill="both")

if __name__ == "__main__":
    root.protocol('WM_DELETE_WINDOW', quit)
    try:
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            # TODO tree does not wrap text
            # TODO remove column bar at the top?
            with open(sys.argv[1]) as f:
                xml = f.read()
        root.mainloop()
    except (KeyboardInterrupt, tk.TclError):
        exit()
