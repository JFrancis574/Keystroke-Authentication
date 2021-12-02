import keyboard
from threading import Timer
from datetime import datetime
import numpy as np
import sqlite3 as sq
import time
import math

from numpy.lib.function_base import append

# Record events until 'esc' is pressed and then plays them
def record():
    startTime = time.time()
    recorded = keyboard.record(until='esc')
    rawKeys = []
    count = 0
    for record in recorded:
        #print(record.name, (record.time - startTime), record.event_type, count)
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
        except IndexError:
            pass;
    return pairsArray
        
    
# Calculate pairs and hold time
def pairs(rawKeys):
    holdTimeArray = []
    for i in range(len(rawKeys)):
        try:
            if (rawKeys[i][2] == 'down' and rawKeys[i+1][2] == 'up' and rawKeys[i][0].lower() == rawKeys[i+1][0].lower()):
                holdTime = rawKeys[i+1][1] - rawKeys[i][1]
                found = False
                for c in holdTimeArray:
                    if c[0] == rawKeys[i][0]:
                        c.append(holdTime)
                        found = True
                if found == False:
                    holdTimeArray.append([rawKeys[i][0], holdTime])
            else:
                for x in range(i, len(rawKeys)):
                    if (rawKeys[x][0].lower() == rawKeys[i][0].lower() and rawKeys[x][2] == 'up' and rawKeys[i][2] == 'down'):
                        holdTime = rawKeys[x][1] - rawKeys[i][1]
                        found = False
                        for c in holdTimeArray:
                            if c[0] == rawKeys[i][0]:
                                c.append(holdTime)
                                found = True
                        if found == False:
                            holdTimeArray.append([rawKeys[i][0], holdTime])        
        except IndexError:
            pass;
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
def KDS(time, keysArray):
    sum = 0
    for i in range(1, len(keysArray)):
        #print(time, keysArray[i][1], keysArray[i][2])
        #print(heaviside(time, keysArray[i][1]) - heaviside(time, keysArray[i][2]))
        sum += heaviside(time, keysArray[i][1]) - heaviside(time, keysArray[i][2])
    #print(time, sum)
    return sum

if __name__ == "__main__":
    rawData = record()
    print("Raw Data:")
    for x in rawData:
        print(x)
        
    rawPairsOut = rawPairs(rawData)
    print("Raw Pairs:")
    for x in rawPairsOut:
        print("Key: " + x[0] + " Down: " + str(x[1]) + " Up: " + str(x[2]))
    
    holdTimes = pairs(rawData)
    print("Pairs with hold times")
    for y in holdTimes:
        for i in range(1, len(y)):
            print("Key: " + y[0] + " Hold time = " + str(y[i]))
        
    avgHoldTimes = avgHoldTime(holdTimes)
    print("Average Hold Times for each key")
    for q in avgHoldTimes:
        print("Key: " + q[0] + " Average hold time: " + str(q[1]))
        
    floattimes = floatTime(rawData)
    print("Floattime - wip")
    for a in floattimes:
        print("Key1: " + a[0] + " Key2: " + a[1] + " Float time = " + str(a[2]))
        
    storeallData(rawData, holdTimes, avgHoldTimes, floattimes)
    
    for x in range(0, 10):
        print(x/10, KDS(x/10, rawPairsOut))
    
    
    
    


