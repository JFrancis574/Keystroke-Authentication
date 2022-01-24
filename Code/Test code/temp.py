# Data in format:
# [key, down, up]
import numpy as np
from math import ceil
import matplotlib.pyplot as plt
from fastdtw import fastdtw
import keyboard
import pickle as p
import time


def heaviside(x1, x2):
    if (x1 > x2):
        return 1
    elif (x1 == x2):
        return 0.5
    else:
        return 0

# KDS function
def KDS(time, keysArray, roundValue):
    sum = 0
    for i in range(1, len(keysArray)):
        sum += heaviside(time, round(keysArray[i][1], roundValue)) - heaviside(time, round(keysArray[i][2], roundValue))
    return sum

keysInput = [
    [
        ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0004, 0.0006], ['l', 0.0006, 0.0007], ['o', 0.0007, 0.0008]
    ],
    [
        ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0007, 0.0009], ['p', 0.0009, 0.0009]
    ]
]

KDSOutput = {}
WordByWord = []
# Need to start at 0.0001 and keep going until 0.0004
# 1 to 4??? then divide by 10000
# print(len(keysInput))
# for i in range(0, len(keysInput)):
#     for x in range(int(keysInput[i][0][1]*10000), int(keysInput[i][len(keysInput[i])-1][2]*10000)+1):
#         KDSOutput[x/10000] = KDS(x/10000, keysInput[i], 4) 
#     print(KDSOutput)
#     WordByWord.append(KDSOutput)

# print(WordByWord)
#plt.plot(KDSOutput.keys(), KDSOutput.values())
#plt.show()

def process(startTime, keys):
    rawKeys = []
    count = 0
    for record in keys:
        count += 1
        rawKeys.append([record.name, (record.time - startTime), record.event_type])
    return rawKeys

def record(interval):
    recorded = []
    print("START")
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    print("STOP")
    keyboard.unhook(keyBoardHook)
    return recorded

temp = []

# for x in range(1):
#     FileName = "Imposter"
#     outfile = open(FileName, 'wb')
#     start = time.time()
#     p.dump(process(start, record(10)), outfile)
#     outfile.close()
    




