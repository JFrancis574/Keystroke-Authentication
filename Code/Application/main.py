from functools import partial
from getpass import getuser
import multiprocessing
import os
import random
import subprocess
import sys
import time
import tkinter

import user_profile as pf
import Interval as i
import keyboard
import Training as t

interval = 10
trainingIterationsAfterTrainPhase = 5

def record(interval):
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

def recordUntil():
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    data = input()
    keyboard.unhook(keyBoardHook)
    return recorded, startTime


def runner(prof):
    count = 0
    while True:
        print("RECORDING")
        data, start = record(interval)
        print("RECORDING STOPPED")
        if len(data) != 0:
            if count < trainingIterationsAfterTrainPhase:
                count += 1
                inter = i.Calculation(data, start, prof, 1)
                decision, index = inter.validation(mode='r')
                print(decision, index)
                if decision == False:
                    return
            else:
                inter = i.Calculation(data, start, prof, 1)
                decision, index = inter.validation(mode='t')
        else:
            pass
        
def threading(prof):
    if button.cget('image') == 'pyimage2':
        button.configure(image=imgPlay)
        button.image = imgPlay
        print("PAUSED")
        cmd='rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)
        for t in threads:
            t.terminate()
    else:
        print("RESUME")
        button.configure(image=imgPause)
        button.image = imgPause
        proc = multiprocessing.Process(target=runner, args=(prof,))
        threads.append(proc)
        proc.start()
        
 
def training():
    training = False
    while training == False:
        print(os.getcwd() + '/Data/'+getuser())
        if not os.path.exists(os.getcwd() + '/Data/'+getuser()):
            trainReps = 2
            prof = pf.User_Profile()
            prof.setNew(True)
            # SHOW UI along with text HERE
            # THEN START recording
            data = open(resource_path('TrainingText.csv'), 'r').read()
            trainingText = random.choice(data.split('}'))
            print(trainingText)  
            for x in range(trainReps):
                print("Enter the following text: After you've finished, press enter")
                print(trainingText)
                dt, startTrain = recordUntil()
                if x == 1:
                    train = t.Training(dt, startTrain, prof, 1, 0)
                    if train.success == False:
                        print("Training failed - restart")
                    else:
                        training = True
                else:
                    trainObject = t.Training(dt, startTrain, prof, 1, 1)
                    _, _ = trainObject.validation(mode='rnl')
                    trainObject.update(trainObject.chosen)
            training = True  
        else:
            prof = pf.User_Profile()
            training = True
    return prof


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    prof = training()
    threads = []
    root = tkinter.Tk()
    imgPause = tkinter.PhotoImage(file = resource_path('Pause.png')).subsample(3,3)
    imgPlay = tkinter.PhotoImage(file = resource_path('Play.png')).subsample(3,3)
    root.title("Play/Pause")
    allowed = 10
    if len(threads) == 0:
        proc = multiprocessing.Process(target=runner, args=(prof,))
        threads.append(proc)
        proc.start()
    startTime = time.time()
    button = tkinter.Button(root, bg='white', fg='black', image=imgPause, command=partial(threading, prof))
    button.pack()
    root.mainloop()
    if len(threads) == 0:
        exit()
    else:
        for t in threads:
            t.terminate()