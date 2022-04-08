from functools import partial
import multiprocessing
import os
import time
import tkinter
from threading import *



def count():
    print("sleep time start")
    for i in range(1000):
        print(i)
        time.sleep(1)
    print("sleep time stop")

def threading():
    print(button.cget('image'))
    # if state == 'Pause':
    if button.cget('image') == 'pyimage2':
        button.configure(image=imgPlay)
        button.image = imgPlay
        # Authenticate here
        for t in threads:
            t.terminate()
    else:
        button.configure(image=imgPause)
        button.image = imgPause
        proc = multiprocessing.Process(target=count, args=())
        threads.append(proc)
        proc.start()
    

if __name__ == '__main__':
    threads = []
    root = tkinter.Tk()
    imgPause = tkinter.PhotoImage(file = os.getcwd()+'/Pause.png').subsample(3,3)
    imgPlay = tkinter.PhotoImage(file = os.getcwd()+'/Play.png').subsample(3,3)
    root.title("Play/Pause")
    allowed = 10
    if len(threads) == 0:
        proc = multiprocessing.Process(target=count, args=())
        threads.append(proc)
        proc.start()
    startTime = time.time()
    # button = tkinter.Button(root, text='Pause', width=14, bg='white', fg='black', command=threading)
    button = tkinter.Button(root, bg='white', fg='black', image=imgPause, command=threading)
    button.pack()
    root.mainloop()
    if len(threads) != 0:
        for t in threads:
            t.terminate()
