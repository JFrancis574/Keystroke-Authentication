from getpass import getuser
import time

import DBConnection as db
import Utilities as util
import Word as w
import profile as pf
import Interval as i
import keyboard

interval = 10

Upf = pf.Profile()
print(Upf.userPath)

def record(interval):
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

def recordUntil(untilKey):
    startTime = time.time()
    recorded = keyboard.record(until=untilKey)
    return recorded, startTime

while True:
    if Upf.newUser == True:
        
    print("RECORDING")
    data, start = record(interval)
    print("NOT RECORDING")
    if len(data) != 0:
        inter = i.Calculation(data, start, Upf)
        print(inter)
        decision, index = inter.validation(mode='r')
        print("CALC DONE")
        print(decision, index)
        if decision == False:
            print("AHHHHHHHHHHHHHHHHHHHHHHHH")
            # IMPLEMENT LOCKOUT
            # Call update function from inter if authentication successful
            # Check if user wants to update word before doing so
            # e.g inter.update(index)
            # Also need an add keyboard func 
            #   - maybe user be able to name?
            #   - In same profile - Different keyboard class 
            # 
            break
        elif decision == 'New':
            Upf = pf.Profile(getuser())

        