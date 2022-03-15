from getpass import getuser
import os
import time

import profile as pf
import Interval as i
import keyboard
import Training as t

interval = 10

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


def runner(prof):
    while True:
        print("RECORDING")
        data, start = record(interval)
        print("RECORDING STOPPED")
        if len(data) != 0:
            inter = i.Calculation(data, start, prof, 1)
            decision, index = inter.validation(mode='r')
            print(decision, index)
            if decision == False:
                return
        else:
            pass
        
 
training = False
while training == False:
    if not os.path.exists(os.getcwd() + '/Data/'+getuser()):
        prof = pf.Profile()
        prof.setNew(True)
        # SHOW UI along with text HERE
        # THEN START recording
        dt, startTrain = recordUntil('esc')
        train = t.Training(dt, startTrain, prof)
        if train.success == False:
            print("Training failed - restart")
        else:
            training = True
    else:
        prof = pf.Profile()
        training = True
        
runner(prof)