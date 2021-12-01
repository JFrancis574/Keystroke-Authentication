import keyboard
from threading import Timer
from datetime import datetime
from numpy import add

from numpy.lib.function_base import append

# Record events until 'esc' is pressed and then plays them
def record():
    recorded = keyboard.record(until='esc')
    print(recorded)
    rawKeys = []
    count = 0
    for record in recorded:
        print(record.name, record.time, record.event_type, count)
        count += 1
        rawKeys.append([record.name, record.time, record.event_type])
    return rawKeys
    
# Calculate pairs and hold time
def pairs(rawKeys):
    holdTimeArray = []
    for i in range(len(rawKeys)):
        try:
            if (rawKeys[i][2] == 'down' and rawKeys[i+1][2] == 'up'):
                holdTime = rawKeys[i+1][1] - rawKeys[i][1]
                found = False
                for c in holdTimeArray:
                    if c[0] == rawKeys[i][0]:
                        c.append(holdTime)
                        found = True
                if found == False:
                    holdTimeArray.append([rawKeys[i][0], holdTime])
            else:
                for x in range(len(rawKeys)):
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

# Calculate float time
def floatTime(rawData):
    for x in range(len(rawData)):
        if (rawData[x][2] == 'up'):
            for i in range(x, len(rawData)):
                if (rawData[i][2] == 'down'):
                    flightime = rawData[i][1] - rawData[x][1]
                    print(rawData[x][0] + " " +  rawData[i][0] + " " + str(flightime))
                    break;
                    
                    
            
    

   
if __name__ == "__main__":
    rawData = record()
    print("Raw Data:")
    for x in rawData:
        print(x)
    
    holdTimes = pairs(rawData)
    print("Pairs")
    for y in holdTimes:
        print("Key: " + y[0] + " Holdtime = " + str(y[1]))
        
    avgHoldTimes = avgHoldTime(holdTimes)
    print("Average Hold Times for each key")
    for q in avgHoldTimes:
        print("Key: " + q[0] + " Average hold time: " + str(q[1]))
        
    floatTime(rawData)
    
    
    
    


