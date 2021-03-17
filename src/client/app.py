#!/usr/bin/env python3

import eel

eel.init('web')  # or the name of your directory


@eel.expose
def test(text):
    print(text)


@eel.expose
def hello_world():
    print("Hello from python")


eel.start('index.html', size=(600, 400), block=False)
# eel.start('index.html', size=)
while True:
    print("I'm a main loop")
    eel.set_tree_data("tree")
    eel.sleep(1.0)
