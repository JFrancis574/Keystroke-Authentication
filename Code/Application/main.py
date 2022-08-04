# OS implementation inside Python Standard Lib
# https://docs.python.org/3/library/os.html
import os

# subprocess implementation inside Python Standard Lib
# https://docs.python.org/3/library/subprocess.html
import subprocess

# threading inside Python Standard Lib
# https://docs.python.org/3/library/threading.html
import threading

# Uses pythons builtin time library
# https://docs.python.org/3/library/time.html
import time

# Tkinter base libary inside python
# https://docs.python.org/3/library/tkinter.html
import tkinter as tk


# functools implementation in Python Standard Lib
# https://docs.python.org/3/library/functools.html
from functools import partial

# getpass implementation inside python standard lib
# https://docs.python.org/3/library/getpass.html
from getpass import getuser

# Implementation by Broppeh
# https://github.com/boppreh/keyboard
import keyboard

import Interval as i
import Training as t
from user_profile import User_Profile

# The main running class. Run everything from here.
interval = 5
trainingItersYN = True
trainingIters = 5

def record(interval):
    """Recording keystrokes function

    Args:
        interval (float): How long to record for

    Returns:
        keystroke data: Comprised of a dictionary
        starttime: Comprised of the starttime of the data
    """
    
    recorded = []
    # Uses pythons builtin time library
    # https://docs.python.org/3/library/time.html
    startTime = time.time()

    # Uses the keyboard lib to unhook and hook the data
    # Implementation by Broppeh
    # https://github.com/boppreh/keyboard
    keyBoardHook = keyboard.hook(recorded.append)
    
    time.sleep(interval)
    
    keyboard.unhook(keyBoardHook)
    
    return recorded, startTime

def runner(id, prof):
    """Is run on the other thread, runs the recording and validation functions.

    Args:
        id (int): ID of the thread
        prof (User_Profile): The User_Profile in use
        stop (bool): The function used to stop the thread
    """
    count = 0
    while True:
        data, start = record(interval)
        if trainingItersYN == False or count > trainingIters:
            inter = i.Calculation(data, start, prof, 1)
            decision, _ = inter.validation(mode='r')
            if decision == 'New':
                prof.addKeyboard(None)
        else:
            if count <= trainingIters and len(data) != 0:
                inter = t.Training(data, start, prof, 1,0)
                count += 1
    
       

    
if __name__ == '__main__':
    prof = User_Profile()
    runner(1,prof)
