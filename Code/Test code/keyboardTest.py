import os
import keyboard
import sqlite3 as sq
import time

from DBConnection import DBStuff
import matplotlib.pyplot as plt
import pickle
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

from setup import setupDone

def recordReg(until):
    startTimeReg = time.time()
    processed = process(startTimeReg, keyboard.record(until))
    if processed == []:
        return False
    else:
        return words(rawPairs(processed))
    
def words(pairs):
    currentWord = []
    output = []
    for i in pairs:
        if i[0] not in [',','!','space', 'enter', ';',"'",'(',')', ',']:
            if i[0] == 'backspace':
                if len(currentWord) != 0:
                    currentWord.pop(len(currentWord)-1)
                else:
                    pass
            elif i[0] == pairs[len(pairs)-1][0]:
                output.append(currentWord)
                currentWord = []
            else:
                currentWord.append(i)
        else:
            output.append(currentWord)
            currentWord = []
    return output

# Record events until at the interval passed in
def record(interval):
    recorded = []
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded

def process(startTime, keys):
    if len(keys) == 0:
        return []
    rawKeys = []
    count = 0
    for record in keys:
        count += 1
        rawKeys.append([record.name, (record.time - startTime), record.event_type])
    return rawKeys
    
# Calculate just pairs
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
        
    
# Calculate pairs and hold time
def holdTime(pairs):
    holdTimeArray = []
    for i in pairs:
        holdTimeCalc = i[2] - i[1]
        found = False
        for c in holdTimeArray:
            if c[0] == i[0]:
                c.append(holdTimeCalc)
                found = True
        if found == False:
            holdTimeArray.append([i[0], holdTimeCalc])
    return holdTimeArray

# Calculate average hold time
def avgHoldTime(holdArray):
    avgHoldTimeArray = []
    for b in holdArray:
        if (len(b)>2):
            addInt = 0.0
            for i in range(1,len(b)):
                addInt += b[i]
            avgHoldTime = float(addInt) / float(len(b))
            avgHoldTimeArray.append([b[0], avgHoldTime])
        else:
            avgHoldTimeArray.append([b[0], b[1]])
    return avgHoldTimeArray

# Calculate float time - not finished
def floatTime(rawData):
    flighTimeArray = []
    for x in range(len(rawData)):
        if (rawData[x][2] == 'up'):
            for i in range(x, len(rawData)):
                if (rawData[i][2] == 'down'):
                    flightime = rawData[i][1] - rawData[x][1]
                    flighTimeArray.append([rawData[x][0], rawData[i][0], flightime])
                    break;
    return flighTimeArray

def floatTime2(data):
    flighTimeArray = []
    for x in range(len(data)):
        try:
            if data[x][2] == 'up' and data[x+1][2] == 'down':
                flightTime = data[x+1][1] - data[x][1]
                flighTimeArray.append([data[x][0], data[x+1][0], flightTime])
            elif data[x][2] == 'down' and data[x+1][2] == 'up':
                pass
                
        except IndexError:
            pass
    return flighTimeArray

# Storing all the data                              
def storeallData(rawData, holdTimes, avgHoldTimes, floatTimes):
    session = 0;
    dbConn = sq.connect("keyStorage.db")
    cursor = dbConn.cursor()
    # Storing all the raw data. Not in full version
    cursor.execute("CREATE TABLE IF NOT EXISTS keyPresses (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, key TEXT, key_action TEXT, time_of_action REAL)")
    
    sessionID = cursor.execute("SELECT MAX(session_id) FROM keyPresses").fetchone()[0]
    if (str(sessionID) != "None"):
        session = sessionID + 1
        for x in rawData:
            cursor.execute("INSERT INTO keyPresses (session_id, key, key_action, time_of_action) VALUES (?, ?, ?, ?)", (session, x[0], x[2], x[1]))
            dbConn.commit()
    else:
        for x in rawData:
            cursor.execute("INSERT INTO keyPresses (session_id, key, key_action, time_of_action) VALUES (?, ?, ?, ?)", (session, x[0], x[2], x[1]))
            dbConn.commit()
    # Sessions
    cursor.execute("CREATE TABLE IF NOT EXISTS sessions (SessionID INTEGER PRIMARY KEY, average_hold_time REAL, average_float_time REAL, session_length_keys INTEGER, session_length_time	REAL)")
    length_keys = 0
    for y in holdTimes:
        for i in range(1, len(y)):
            length_keys +=1
    length_time = rawData[len(rawData)-1][1] - rawData[0][1]
    totalHold = 0
    countHold = 0
    for i in avgHoldTimes:
        totalHold += i[1]
        countHold += 1
    sessionAvgHoldTime = totalHold/countHold
    
    totalFloat = 0
    countFloat = 0
    for i in floatTimes:
        totalFloat += i[2]
        countFloat += 1
    sessionAvgFloatTime = totalFloat/countFloat
    cursor.execute("INSERT INTO sessions (SessionID, average_hold_time, average_float_time, session_length_keys, session_length_time) VALUES (?,?, ?, ?, ?)", (session, sessionAvgHoldTime, sessionAvgFloatTime, length_keys, length_time))
    dbConn.commit()
    
    # Pairs
    cursor.execute("CREATE TABLE IF NOT EXISTS pairs (pair_id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, key TEXT, holdtime REAL)")
    for x in holdTimes:
        for i in range(1, len(x)):
            cursor.execute("INSERT INTO pairs (session_id, key, holdtime) VALUES (?, ?, ?)", (session, x[0], x[i]))
            dbConn.commit()

# Heaviside function used for KDS
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
    for i in range(0, len(keysArray)):
        sum += heaviside(time, round(keysArray[i][1], roundValue)) - heaviside(time, round(keysArray[i][2], roundValue))
    return sum

def KDSWordByWord(wordsOut, roundValue):
    KDSOutput = {}
    WordByWord = []
    for i in range(0, len(wordsOut)):
        if len(wordsOut[i]) != 0:
            for x in range(int(wordsOut[i][0][1]*10000), int(wordsOut[i][len(wordsOut[i])-1][2]*10000)+1):
                KDSOutput[x/10000] = KDS(x/10000, wordsOut[i], roundValue) 
            WordByWord.append([i,KDSOutput])
            KDSOutput = {}
    return WordByWord

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
            if words[i] == []:
                pass
            elif wordChooseInterval+banding >= diff:
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

# Test words data visualisation:
# words = [
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

if __name__ == "__main__":
    interval = 60.0
    
    infile = open(os.getcwd()+"/Data/Pickles/Hello1",'rb')
    processed1 = pickle.load(infile)
    infile.close()
    
    infile = open(os.getcwd()+"/Data/Pickles/Hello2",'rb')
    processed2 = pickle.load(infile)
    infile.close()
    
    infile = open(os.getcwd()+"/Data/Pickles/Imposter",'rb')
    processed3 = pickle.load(infile)
    infile.close()
    
    for x in range(1):
        rawPairsOut = rawPairs(processed1)
        rawPairsOut1 = rawPairs(processed2)
        rawPairsOut2 = rawPairs(processed3)
        
        wordsOut = KDSWordByWord(words(rawPairsOut), 4)
        wordsOut1 = KDSWordByWord(words(rawPairsOut1), 4)
        wordsOut2 = KDSWordByWord(words(rawPairsOut2), 4)

        first = np.array(list(wordsOut[0][1].values()))
        second = np.array(list(wordsOut1[0][1].values()))
        third = np.array(list(wordsOut2[0][1].values()))
        
        distance, path = fastdtw(first, second, dist=euclidean)
        distance2, path2 = fastdtw(first, third, dist=euclidean)
        
        print("Distance between 1 and 2 is " + str(distance))
        print("Distance between 1 and 3 is " + str(distance2))
        
        f_path, s_path = zip(*path)
        f_path = np.asarray(f_path)
        s_path = np.asarray(s_path)
        f_warped = first[f_path]
        s_warped = second[s_path]
        
        f_path2, t_path2 = zip(*path)
        f_path2 = np.asarray(f_path2)
        t_path2 = np.asarray(t_path2)
        f_warped2 = first[f_path2]
        t_warped2 = third[t_path2]
        
        print(len(f_warped), len(np.array(list(wordsOut[0][1].keys()))))
        print(len(s_warped), len(np.array(list(wordsOut1[0][1].keys()))))
        print(len(t_warped2), len(np.array(list(wordsOut2[0][1].keys()))))
        
        warpedKeys = [i/10000 for i in range(1, len(f_warped)+1)]
        
        corr = np.corrcoef(f_warped, s_warped)
        corr2 = np.corrcoef(f_warped2, t_warped2)
        
        print("High is good, a value above 0.4 means a strong positive while a value of 1 means a perfect strong positive correlation")
        print("0.00 means no correlation - e.g. not the same user")
        # http://academic.brooklyn.cuny.edu/soc/courses/712/chap18.html
        print(corr[0,1], corr2[0,1])
        
        fig, axs = plt.subplots(3,2)
        axs[0, 0].plot(wordsOut[0][1].keys(), wordsOut[0][1].values(), color="blue")
        axs[0, 0].grid(True)
        axs[0, 0].set_title("BEFORE DTW: 1")
            
        axs[1, 0].plot(wordsOut1[0][1].keys(), wordsOut1[0][1].values(), color="orange")
        axs[1, 0].grid(True)
        axs[1, 0].set_title("BEFORE DTW: 2")
        
        axs[2, 0].plot(wordsOut2[0][1].keys(), wordsOut2[0][1].values(), color="purple")
        axs[2, 0].grid(True)
        axs[2, 0].set_title("BEFORE DTW: 3")
        
        axs[0, 1].plot(warpedKeys,f_warped, color="blue")
        axs[0, 1].grid(True)
        axs[0, 1].set_title("After DTW: 1")
            
        axs[1, 1].plot(warpedKeys,s_warped, color="orange")
        axs[1, 1].grid(True)
        axs[1, 1].set_title("After DTW: 2")
        
        axs[2, 1].plot(warpedKeys,t_warped2, color="purple")
        axs[2, 1].grid(True)
        axs[2, 1].set_title("After DTW: 3")
        
        plt.show()
        
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(wordsOut[0][1].keys(), wordsOut[0][1].values(), color="orange", label="Genuine")
        ax[0].plot(wordsOut1[0][1].keys(), wordsOut1[0][1].values(), color="blue", label="Genuine")
        ax[0].plot(wordsOut2[0][1].keys(), wordsOut2[0][1].values(), color="purple", label="Imposter")
        ax[0].grid(True)
        ax[0].legend(loc=5)
        ax[0].set_title("Pre-DTW")
        
        ax[1].plot(warpedKeys,f_warped, color="blue", label="Genuine")
        ax[1].plot(warpedKeys,s_warped, color="orange", label="Genuine")
        ax[1].plot(warpedKeys,t_warped2, color="purple", label="Imposter")
        ax[1].grid(True)
        ax[1].legend(loc=5)
        ax[1].set_title("Post-DTW")
        
        plt.show()

""" 
TODO:
- Second stage of algorithm
    - Not much progress made 
"""   


