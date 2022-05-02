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
interval = 60
trainingItersYN = True
trainingIters = 5

def record(interval, stop):
    """Recording keystrokes function

    Args:
        interval (float): How long to record for

    Returns:
        keystroke data: Comprised of a dictionary
        starttime: Comprised of the starttime of the data
    """
    if stop():
        return None, None
    recorded = []
    # Uses pythons builtin time library
    # https://docs.python.org/3/library/time.html
    startTime = time.time()

    # Uses the keyboard lib to unhook and hook the data
    # Implementation by Broppeh
    # https://github.com/boppreh/keyboard
    keyBoardHook = keyboard.hook(recorded.append)
    if stop():
        return None, None
    x = 0 
    while x <= interval:
        # Used instead of time.sleep due to need to stop.
        # Program would hang if thread was closed whilst recording
        if stop():
            return None, None
        time.sleep(1)
        if stop():
            return None, None
        x += 1
    
    keyboard.unhook(keyBoardHook)
    if stop():
        return None, None
    return recorded, startTime

def resource_path(relative_path):
    """When using the installer, stores files in a different temp location

    Args:
        relative_path (string): Name of the file

    Returns:
        path: The path to the object
    """
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)

def stop():
    """Changes the image on button press. Also stops and starts the validation thread
    """
    global stop_threads
    if button.cget('image') == 'pyimage2':
        cmd='rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)
        button.configure(image=imgPlay)
        button.image = imgPlay
        stop_threads = True
        for thread in threads:
            thread.join()
    else:
        button.configure(image=imgPause)
        button.image = imgPause
        stop_threads = False
        tmp = threading.Thread(target=runner, args=(0, prof, lambda: stop_threads))
        tmp.start()

def runner(id, prof, stop):
    """Is run on the other thread, runs the recording and validation functions.

    Args:
        id (int): ID of the thread
        prof (User_Profile): The User_Profile in use
        stop (bool): The function used to stop the thread
    """
    count = 0
    while True:
        data, start = record(interval, lambda: stop_threads)
        if stop():
            break
        if trainingItersYN == False or count > trainingIters:
            inter = i.Calculation(data, start, prof, 1, lambda: stop_threads)
            if stop():
                break
            decision, _ = inter.validation(mode='r')
            if decision == 'New':
                prof.addKeyboard(None)
        else:
            if count <= trainingIters and len(data) != 0:
                inter = t.Training(data, start, prof, 1,0, lambda: stop_threads)
                count += 1
                if stop():
                    break
    
def getInp(keyboardHook, inpText, root):
    """Function used to get the input from the training UI

    Args:
        keyboardHook (Hook): KeyboardHook object to unbind
        inpText (UI Element): The UI element to get the text from
        root (tkinter): The Tkinter object 
    """
    input = inpText.get("1.0",'end-1c')
    if len(input) == 0:
        return
    else:
        keyboard.unhook(keyboardHook)
        root.destroy()
       
def training():
    """Runs all training procedures

    Returns:
        User_profile: A new User_Profile with the learnt data inside
    """
    
    if not os.path.exists(os.getcwd() + '/Data/'+getuser()):
        # If the user doesn't exists already
        # Create a new profile and set the new flag
        prof = User_Profile()
        prof.setNew(True)

        # Grab the training text from the file
        # Training text is:
        # H. W. Dodge, The geology of Darling State Park. Montpelier: Vermont Geological Survey, 1967. 
        file = open(resource_path('TrainingText.csv'))
        content = file.read()
        file.close()

        recorded = []

        # Referenced above
        start = time.time()
        keyboardHook = keyboard.hook(recorded.append)

        # Tkinter base libary inside python
        # https://docs.python.org/3/library/tkinter.html
        root = tk.Tk()
        root.title("TRAINING")
        l = tk.Label(text=content)
        inpText = tk.Text(root)
        button = tk.Button(root, text='Enter', bg='white', fg='black', command=partial(getInp, keyboardHook, inpText, root))
        l.pack()
        inpText.pack()
        button.pack()
        root.mainloop()

        train = t.Training(recorded, start, prof, 1, 0, lambda: stop_threads)

        if train.success == True:
            # If Training succeds return and start the main program
            return prof
        else:  
            # Otherwise loop back round
            root.mainloop()
            return User_Profile()
    else:
        global trainingItersYN
        trainingItersYN = False
        return User_Profile()
    
    
if __name__ == '__main__':
    global stop_threads
    stop_threads = False
    prof = training()
    threads = []
    id = 0
    tmp = threading.Thread(target=runner, args=(id, prof, lambda: stop_threads))
    threads.append(tmp)
    tmp.start()
    root = tk.Tk()
    imgPause = tk.PhotoImage(file = resource_path('Pause.png')).subsample(3,3)
    imgPlay = tk.PhotoImage(file = resource_path('Play.png')).subsample(3,3)
    root.title("Play/Pause")
    button = tk.Button(root, bg='white', fg='black', image=imgPause, command=stop)
    button.pack()
    root.mainloop()
    stop_threads = True
    for thread in threads:
        thread.join()
