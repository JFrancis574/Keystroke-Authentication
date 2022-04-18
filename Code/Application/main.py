from functools import partial
from getpass import getuser
import os
import subprocess
import sys
import threading
import time
from tkinter import ttk
import keyboard
import tkinter as tk
import Interval as i
import Training as t
from user_profile import User_Profile

interval = 5
trainingItersYN = False
trainingIters = 5

def record(interval):
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def stop():
    global stop_threads
    if button.cget('image') == 'pyimage2':
        cmd='rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)
        print("PAUSE")
        button.configure(image=imgPlay)
        button.image = imgPlay
        stop_threads = True
        for worker in workers:
            worker.join()
        print(workers)
        print('Finis.')
    else:
        print("RESUME")
        button.configure(image=imgPause)
        button.image = imgPause
        stop_threads = False
        tmp = threading.Thread(target=runner, args=(0, prof, lambda: stop_threads))
        tmp.start()

def runner(id, prof, stop):
    count = 0
    while True:
        print("RECORDING")
        data, start = record(interval)
        if stop():
            print("EXITING")
            break
        print("STOPPING")
        if stop():
            print("EXITING")
            break
        if trainingItersYN == False:
            inter = i.Calculation(data, start, prof, 1)
            print(inter.noWords)
            if stop():
                print("EXITING")
                break
            decision, index = inter.validation(mode='r')
            print(decision, index)
            if decision == False:
                break
        else:
            if count <= trainingIters:
                inter = t.Training(data, start, prof, 1,0)
                count += 1
                if stop():
                    print("EXITING")
                    break
    print("END")
    
def getInp(keyboardHook, inpText, root):
    input = inpText.get("1.0",'end-1c')
    if len(input) == 0:
        return
    else:
        print(input)
        keyboard.unhook(keyboardHook)
        root.destroy()
       
def training():
    if not os.path.exists(os.getcwd() + '/Data/'+getuser()):
        prof = User_Profile()
        prof.setNew(True)
        file = open('TrainingText.csv')
        content = file.read()
        file.close()
        recorded = []
        start = time.time()
        keyboardHook = keyboard.hook(recorded.append)
        root = tk.Tk()
        root.title("TRAINING")
        l = tk.Label(text=content)
        inpText = tk.Text(root)
        button = tk.Button(root, text='Enter', bg='white', fg='black', command=partial(getInp, keyboardHook, inpText, root))
        l.pack()
        inpText.pack()
        button.pack()
        root.mainloop()
        print(recorded)
        root = tk.Tk()
        root.title("TRAINING") 
        pb = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=280)
        pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        pb.start()
        print("HERE")
        train = t.Training(recorded, start, prof, 1, 0)
        if train.success == True:
            print("Training Done")
            root.destroy()
            return prof
        else:  
            root.mainloop()
            return User_Profile()
    else:
        return User_Profile()
    
    
if __name__ == '__main__':
    prof = training()
    global stop_threads
    stop_threads = False
    workers = []
    id = 0
    tmp = threading.Thread(target=runner, args=(id, prof, lambda: stop_threads))
    workers.append(tmp)
    tmp.start()
    root = tk.Tk()
    imgPause = tk.PhotoImage(file = resource_path('Pause.png')).subsample(3,3)
    imgPlay = tk.PhotoImage(file = resource_path('Play.png')).subsample(3,3)
    root.title("Play/Pause")
    button = tk.Button(root, bg='white', fg='black', image=imgPause, command=stop)
    button.pack()
    root.mainloop()
    stop_threads = True
    for worker in workers:
        worker.join()