import time

from numpy import empty
import DBConnection as db
import Utilities as util
import Word as w
import WordProcessing as wp
import profile as pf
import Interval as i
import keyboard

interval = 10

def record(interval):
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

Upf = pf.Profile("Jack", "Pass")
print(Upf.userPath)

while True:
    print("RECORDING")
    data, start = record(interval)
    print("NOT RECORDING")
    if len(data) != 0:
        inter = i.Calculation(data, start, Upf)
        print(inter.toString())
        decision, index = inter.validation(mode='t')
        print("CALC DONE")
        print(decision, index)
        if decision == False:
            print("AHHHHHHHHHHHHHHHHHHHHHHHH")
            print(index)
            break
        