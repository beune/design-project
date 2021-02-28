import tkinter as tk
import tkinter.ttk
import sys
import os
from src.refined_gui.custom_windows_bar import CustomTitleBar
from src.refined_gui.menu_ribbon import MenuRibbon
from src.refined_gui.title_bar import TitleBar
from src.refined_gui.main_canvas import MainCanvas
import constants

"""Main window"""
root = tk.Tk()  # create main window
root_width = int(root.winfo_screenwidth() / 2)
root_height = root.winfo_screenheight()
root.geometry(str(root_width) + 'x' + str(root_height))  # set size of window
root.title('Radio')  # set title
root.iconbitmap(constants.IMAGE_PATH + '\logo.ico')  # set icon

"""Menu ribbon"""
menu_ribbon = MenuRibbon(root)

"""Title bar"""
title_bar = TitleBar(root)

"""Main canvas"""
main_canvas = MainCanvas(root)

if __name__ == "__main__":
    root.protocol('WM_DELETE_WINDOW', quit)
    try:
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            with open(sys.argv[1]) as f:
                xml = f.read()
        root.mainloop()
    except (KeyboardInterrupt, tk.TclError):
        exit()
