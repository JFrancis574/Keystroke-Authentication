import keyboard
from threading import Timer
from datetime import datetime
from numpy import add

from numpy.lib.function_base import append

# Record events until 'esc' is pressed and then plays them
recorded = keyboard.record(until='esc')
print(recorded)
rawKeys = []
holdTimeArray = []
avgHoldTimeArray = []
count = 0
for record in recorded:
    print(record.name, record.time, record.event_type, count)
    count += 1
    rawKeys.append([record.name, record.time, record.event_type])
    
print("Raw Data:")
for x in rawKeys:
    print(x)

print("Pairs:")
for i in range(len(rawKeys)):
    try:
        if (rawKeys[i][2] == 'down' and rawKeys[i+1][2] == 'up'):
            holdTime = rawKeys[i+1][1] - rawKeys[i][1]
            print("Key: " + rawKeys[i][0] + " Holdtime = " + str(holdTime))
            found = False
            for c in holdTimeArray:
                if c[0] == rawKeys[i][0]:
                    c.append(holdTime)
                    found = True
            if found == False:
                holdTimeArray.append([rawKeys[i][0], holdTime])
    except IndexError:
        pass;

print("Hold Times for each key:")
for b in holdTimeArray:
    print(b)
    if (len(b)>2):
        addInt = 0.0
        for i in range(1,len(b)):
            addInt += b[i]
        avgHoldTime = float(addInt) / float(len(b))
        avgHoldTimeArray.append([b[0], avgHoldTime])

print("Average Hold Times for each key")
for q in avgHoldTimeArray:
    print("Key: " + q[0] + " Average hold time: " + str(q[1]))
