from getpass import getuser
import os
import random
import time
import tkinter

import user_profile as pf
import Interval as i
import keyboard
import Training as t

interval = 60
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
        
 
training = False
while training == False:
    if not os.path.exists(os.getcwd() + '/Data/'+getuser()):
        trainReps = 2
        prof = pf.User_Profile()
        prof.setNew(True)
        # SHOW UI along with text HERE
        # THEN START recording
        data = open('TrainingText.csv', 'r').read()
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
        
runner(prof)