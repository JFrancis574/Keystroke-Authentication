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
    ],
    [
        ['j', 0.0010, 0.0011], ['a', 0.0013, 0.0014], ['c', 0.0017, 0.0020], ['k', 0.0022, 0.0025]
    ],
    [
        ['g', 0.0027, 0.0030], ['a', 0.0035, 0.0044], ['c', 0.0050, 0.0070], ['k', 0.0072, 0.0075]
    ]
]

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

def rawPairs(rawKeys):
    pairsArray = []
    for i in range(len(rawKeys)):
        try:
            if (rawKeys[i][2] == 'down' and rawKeys[i+1][2] == 'up' and rawKeys[i][0].lower() == rawKeys[i+1][0].lower()):
                pairsArray.append([rawKeys[i][0], rawKeys[i][1], rawKeys[i+1][1]])
            else:
                for x in range(i, len(rawKeys)):
                    if (rawKeys[x][0].lower() == rawKeys[i][0].lower() and rawKeys[x][2] == 'up' and rawKeys[i][2] == 'down'):
                        pairsArray.append([rawKeys[i][0], rawKeys[i][1], rawKeys[x][1]])
                        break        
        except IndexError:
            pass;
    return pairsArray

def words(pairs):
    currentWord = []
    output = []
    for i in pairs:
        if i[0] not in [',','!','space', 'enter', ';',"'",'(',')', ',']:
            if i[0] == 'backspace':
                currentWord.pop(len(currentWord)-1)
            elif i[0] == pairs[len(pairs)-1][0]:
                output.append(currentWord)
                currentWord = []
            else:
                currentWord.append(i)
        else:
            output.append(currentWord)
            currentWord = []
    return output

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
    

def wordChoose(words, amountofWords, banding=0):
    wordCount = len(words)
    if (wordCount == 0 or amountofWords == 0):
        return []
    elif wordCount < amountofWords:
        return []
    elif wordCount == amountofWords:
        return words
    else:
        diff = words[-1][-1][2] - words[0][0][1]
        out = []
        wordChooseInterval = diff/amountofWords
        og = diff/amountofWords
        count = 0
        for i in range(0, wordCount):
            if wordChooseInterval+banding >= diff:
                break
            elif words[i][0][1] <= (wordChooseInterval+banding) and words[i][-1][2] >= (wordChooseInterval+banding):
                count+=1
                out.append(words[i])
                wordChooseInterval += og + banding
            else:
                pass
        if len(out) != amountofWords:
            if len(out) == amountofWords-1:
                y = int(round(len(out)/2, 0))
                inputWord = words[y]
                for x in range(0, len(out)):
                    if inputWord == out[x]:
                        inputWord = words[y+1]
                out.append(inputWord)
                return out
            else:
                return wordChoose(words, amountofWords, banding+0.1)
        else:
            return out
        

# keysInput = [
#     [
#         ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0004, 0.0006], ['l', 0.0006, 0.0007], ['o', 0.0007, 0.0008]
#     ],
#     [
#         ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0007, 0.0009], ['p', 0.0009, 0.0009]
#     ],
#     [
#         ['j', 0.0010, 0.0011], ['a', 0.0013, 0.0014], ['c', 0.0017, 0.0020], ['k', 0.0022, 0.0025]
#     ],
#     [
#         ['g', 0.0027, 0.0030], ['a', 0.0035, 0.0044], ['c', 0.0050, 0.0070], ['k', 0.0072, 0.0075]
#     ]
# ]


infile = open("60SecondTestData",'rb')
processed1 = p.load(infile)
infile.close()
wordsOut = words(rawPairs(processed1))
#print(wordsOut[0:2])
chosen = wordChoose(wordsOut, 4)

for i in chosen:
    print(i)

for x in range(0, len(wordsOut)):
    if wordsOut[x][0][1] <= 29.640340328216553 and wordsOut[x][-1][2] >= 29.640340328216553:
        print(1)
    elif wordsOut[x][0][1] <= (29.640340328216553+5.0) and wordsOut[x][-1][2] >= (29.640340328216553+5.0):
        print(2)