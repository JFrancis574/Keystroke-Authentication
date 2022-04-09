from getpass import getuser
from os.path import exists
from os import getcwd
from random import choice
import time
import tkinter as tk
from tkinter import ttk
import keyboard
import user_profile as pf
import Training as t

def recordUntil():
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    data = input()
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

def getInp():
    input = inpText.get("1.0",'end-1c')
    if len(input) == 0:
        return
    else:
        print(input)
        keyboard.unhook(keyboardHook)
        print(recorded)
        root.destroy()
        
if __name__ == '__main__':
    if not exists(getcwd() + '/Data/'+getuser()):
        prof = pf.User_Profile()
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
        button = tk.Button(root, text='Enter', bg='white', fg='black', command=getInp)
        l.pack()
        inpText.pack()
        button.pack()
        root.mainloop()
        
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
        else:  
            root.mainloop()
        
        
        
def Training():
    
    
    