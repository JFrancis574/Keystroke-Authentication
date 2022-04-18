import os
import sys
import threading
import time
import tkinter as tk
from functools import partial

# import keyboard


# def record(interval):
#     recorded = []
#     startTime = time.time()
#     keyBoardHook = keyboard.hook(recorded.append)
#     print("RECORDING")
#     time.sleep(interval)
#     keyboard.unhook(keyBoardHook)
#     print("NOT")
#     return recorded, startTime

# times = {}
# # data, start = record(60)
# # print(start)

# file = open("data.pickle", 'rb')
# data = pickle.load(file)
# start = 1649857380.5629547
# prof = pf.User_Profile()
# presave = t.Training(data, start, prof, 1, 0)

# # file = open("data.pickle", 'wb')
# # pickle.dump(data, file)
# # file.close()
  
# interval = i.Calculation(data, start, prof, 1)
# for x in range(2, interval.noWords, 2):
#     print(x)
#     interval.chosenAmount = x
#     interval.chosen = interval.choose()
#     start = timeit.default_timer()
#     _, _ = interval.validation(mode='rnl')
#     times[x] = timeit.default_timer() - start

# sns.regplot(x=list(times.keys()), y=list(times.values()), ci=None)
# plt.title("Words Chosen vs Time Taken")
# plt.xlabel("Words Chosen")
# plt.ylabel("Time Taken")
# plt.show()

def pausePlay():
    if button.cget('image') == 'pyimage2':
        print("PAUSE")
        pause = True
        button.configure(image=imgPlay)
        button.image = imgPlay
    else:
        print("RESUME")
        button.configure(image=imgPause)
        button.image = imgPause
        
        
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# pause = False
# root = tk.Tk()
# imgPause = tk.PhotoImage(file = resource_path('Pause.png')).subsample(3,3)
# imgPlay = tk.PhotoImage(file = resource_path('Play.png')).subsample(3,3)
# count()
# root.title("Play/Pause")
# startTime = time.time()
# button = tk.Button(root, bg='white', fg='black', image=imgPause, command=pausePlay)
# button.pack()
# root.mainloop()
# count()

# Create Object
# root = tk.Tk()
  
# # Set geometry
# root.geometry("400x400")
  
# # use threading
  
# def Threading():
#     # Call work function
#     t1=threading.Thread(target=work)
#     t1.start()
    
  
# # work function
# def work():
#     print("sleep time start")
  
#     for i in range(10):
#         print(i)
#         time.sleep(1)
  
#     print("sleep time stop")
  
# # Create Button
# tk.Button(root,text="Click Me",command = Threading).pack()
  
# # Execute Tkinter
# root.mainloop()

def stop():
    global stop_threads
    if button.cget('image') == 'pyimage2':
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
        tmp = threading.Thread(target=do_work, args=(0, lambda: stop_threads))
        tmp.start()
        
    
def do_work(id, stop):
    print("ID:", id)
    x = 0
    while True:
        print(x)
        time.sleep(x)
        x += 1
        if stop():
            print("EXITING")
            break
    print("STOPPING")
    
def Training():
    trainRoot = tk.Tk()
    


if __name__ == '__main__':
    prof = Training()
    quit()
    global stop_threads
    stop_threads = False
    workers = []
    id = 0
    tmp = threading.Thread(target=do_work, args=(id, lambda: stop_threads))
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









