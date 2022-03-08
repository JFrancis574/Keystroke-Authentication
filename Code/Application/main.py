from getpass import getuser
import time

import profile as pf
import Interval as i
import keyboard
import Training as t

interval = 10

Upf = pf.Profile('Keyboard1 ')
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
        print("Recording Training: ")
        dt, startTrain = recordUntil('esc')
        print("NOT Recording Training: ")
        t.Training(dt, startTrain, Upf)
        print("Training DONE")
        Upf.setNew(False)
        Upf.addKeyboard(input("Keyboard Name: "))
        
    print("RECORDING")
    data, start = record(interval)
    print(data)
    for x in data:
        print(x.time)
    print("NOT RECORDING")
    if len(data) != 0:
        inter = i.Calculation(data, start, Upf, 1)
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

        