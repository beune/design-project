#!/usr/bin/env python3

import eel

eel.init('web')  # or the name of your directory


@eel.expose
def test(text):
    print(text)


@eel.expose
def hello_world():
    print("Hello from python")


eel.start('index.html', size=(600, 400))
# eel.start()
