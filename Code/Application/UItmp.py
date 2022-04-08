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
    if button['text'] == 'Pause':
        button.configure(text='Play')
        # Authenticate here
        for t in threads:
            t.terminate()
    else:
        button.configure(text='Pause')
        proc = multiprocessing.Process(target=count, args=())
        threads.append(proc)
        proc.start()


if __name__ == '__main__':
    threads = []
    root = tkinter.Tk()
    root.title("Play/Pause")
    allowed = 10
    if len(threads) == 0:
        proc = multiprocessing.Process(target=count, args=())
        threads.append(proc)
        proc.start()
    startTime = time.time()
    button = tkinter.Button(root, text='Pause', width=14, bg='white', fg='black', command=threading)
    button.pack()
    root.mainloop()
    if len(threads) != 0:
        for t in threads:
            t.terminate()
