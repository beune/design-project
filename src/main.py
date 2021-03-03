#!/usr/bin/env python3
"""
Imports
"""
import eel

# Set web files folder
eel.init('web')


@eel.expose  # Expose this function to Javascript
def say_hello_py(x):
    """

    :param x:
    """
    print('Hello from %s' % x)


say_hello_py('Python World!')
eel.say_hello_js('Python World!')  # Call a Javascript function

eel.start('hello.html', size=(300, 200))  # Start
# eel.start('hello.html', size=(300, 200))  # Start
