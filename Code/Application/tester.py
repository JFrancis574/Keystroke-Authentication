import json
import user_profile as p
import os
import time as t
from Interval import Calculation
import timeit

from sys import platform

if platform == 'darwin':
    import keyboardEvent as k
else:
    import keyboard as k

def testerDataFormer(string, holdTime, floatTime, file=0, variable=0):
    output = []
    if file == 0:
        data = string
    else:
        if os.path.exists(os.getcwd()+string):
            data = open(string, 'r')
        else:
            return
    
    if isinstance(holdTime, float) and isinstance(floatTime, float):
        time = t.time()
        for x in data:
            output.append(k.KeyboardEvent('down', 99, name=x, time=time))
            time+= holdTime
            output.append(k.KeyboardEvent('up', 99, name=x, time=time))
            time += floatTime
        return output
    elif isinstance(holdTime, list) and isinstance(floatTime, float):
        if len(holdTime) > len(data):
            return
        else:
            time = t.time()
            for i in range(len(data)):
                output.append(k.KeyboardEvent('down', 99, name=data[i], time=time))
                time+= holdTime[i]
                output.append(k.KeyboardEvent('up', 99, name=data[i], time=time))
                time += floatTime
            return output
    elif isinstance(holdTime, float) and isinstance(floatTime, list):
        if len(floatTime) > len(data):
            return
        else:
            time = t.time()
            for i in range(len(data)):
                output.append(k.KeyboardEvent('down', 99, name=data[i], time=time))
                time+= holdTime
                output.append(k.KeyboardEvent('up', 99, name=data[i], time=time))
                time += floatTime[i]
            return output
    else:
        if (len(holdTime) > len(data)) or (len(floatTime) > len(data)):
            return
        else:
            time = t.time()
            for i in range(len(data)):
                output.append(k.KeyboardEvent('down', 99, name=data[i], time=time))
                time+= holdTime[i]
                output.append(k.KeyboardEvent('up', 99, name=data[i], time=time))
                time += floatTime[i]
            return output
        
def multipleTestRunner(Teststring, iterations, imposterCount, genuineHoldData, genuineFloatData, imposterHoldData, imposterFloatData, benchmark=0):
    if iterations == 0 or Teststring == "":
        return
    pf = p.Profile('Test')
    
    if benchmark == 0:
         # No benchmark exists
        print("Creating Benchmark")
        # iterations -= 1
        startCount = 1
       
        if isinstance(Teststring, str):
            start = t.time()
            data = testerDataFormer(Teststring, genuineHoldData[0], genuineFloatData[0], 0, 0)
        else:
            start = t.time()
            data = testerDataFormer(Teststring[0], genuineHoldData[0], genuineFloatData[0], 0, 0)

        bench, index = Calculation(data, start, pf, 1).validation(mode='t')
        if bench != "Bench Created":
            return     
    else:
        startCount = 0   
         
    count = 0
    output = {}
    for i in range(startCount, iterations):
        print("Doing Test: ", i)
        start_time = timeit.default_timer()
        if count < imposterCount:
            if isinstance(Teststring, str):
                start = t.time()
                data = testerDataFormer(Teststring, imposterHoldData[i], imposterFloatData[i], 0, 0)
                type = False
                count +=1
            else:
                start = t.time()
                data = testerDataFormer(Teststring[i], imposterHoldData[i], imposterFloatData[i], 0, 0)
                type = False
                count +=1
            print("Hold, Float: ", imposterHoldData[i], imposterFloatData[i])
        else:
            if isinstance(Teststring, str):
                start = t.time()
                data = testerDataFormer(Teststring, genuineHoldData[i],genuineFloatData[i], 0, 0)
                type = True
            else:
                start = t.time()
                data = testerDataFormer(Teststring[i], genuineHoldData[i],genuineFloatData[i], 0, 0)
                type = True
            print("Hold, Float: ", genuineHoldData[i],genuineFloatData[i])
            
        inter = Calculation(data, start, pf, 1)
        decision, index = inter.validation(mode='rnl')
        if decision == type:
            print(i, "Expected Result: " + str(type) + ". Actual Result: " +  str(decision) + ". Test passed!")
            output[i] = type, True
        else:
            print(i, "Expected Result: " +  str(type) + ". Actual Result: " +  str(decision) + ". Test Failed!")
            print(i, "Values Failed: ", index)
            output[i] = type, False
        print(i, " took ", timeit.default_timer() - start_time)
    return output


def multipleTestRunnerVariable(string, midValueHold, midValueFloat, variableAmountHold, variableAmountFloat, testAmount):
    if string == "":
        return
    elif midValueHold - variableAmountHold < 0 or midValueFloat - variableAmountFloat < 0:
        return
    pf = p.User_Profile('Test')
    start = t.time()
    data = testerDataFormer(string, midValueHold, midValueFloat, 0, 0)
    print(midValueHold, midValueFloat)
    _, _ = Calculation(data, start, pf, 1).validation(mode='t')
    minValueHold, minValueFloat = midValueHold - variableAmountHold, midValueFloat - variableAmountFloat
    maxValueHold, maxValueFloat = midValueHold + variableAmountHold, midValueFloat + variableAmountFloat
    everyXHold, everyXFloat = (maxValueHold - minValueHold)/testAmount, (maxValueFloat - minValueFloat)/testAmount
    output = {}
    countHold, countFloat, count = minValueHold+everyXHold, minValueFloat+everyXFloat, 0
    while round(countHold, 2) <= maxValueHold and round(countFloat, 2) <= maxValueFloat and count <= testAmount:
        print("Doing test: ",count)
        start = t.time()
        data = testerDataFormer(string, countHold, countFloat, 0,0)
        inter = Calculation(data, start, pf, 1)
        decision, _ = inter.validation(mode='rnl')
        output[count] = (countHold, countFloat, decision)
        countHold += everyXHold
        countFloat += everyXFloat
        count += 1
    return output
        
    
def displayDictNice(dict, roundValue):
    if len(list(dict.keys())) == 0:
        return
    print("TNO: HT: FT: D:")
    values = list(dict.values())
    for i in range(len(list(dict.keys()))):
        print(i, round(values[i][0], roundValue), round(values[i][1], roundValue), values[i][2])
    
    
    

def decompress(data):
        """Used to decompress the data that is stored in and convert it into the required dictionary

        Args:
            data (dictionary): The compressed data

        Returns:
            dict: The uncompressed data, very large
        """
        outDict = {}
        multiplier = int(str(1) + 4*str(0))
        multiplierPlus1 = int(str('11') + str(int(4-1)*'0'))
        for x in data:
            startTime = list(x.values())[0][0]
            endTime = list(x.values())[0][1]
            value = list(x.values())[1]
            for x in range(int(startTime*multiplier), int(endTime*multiplierPlus1)+1):
                outDict[x/multiplier] = value
        return outDict
            
# out = multipleTestRunner("geographically", 10, 5, [0.1, 0.1, 0.15, 0.125, 0.12, 0.11, 0.09, 0.1, 0.099, 0.1], [0.01, 0.015, 0.02, 0.012, 0.013, 0.014, 0.013, 0.011, 0.02, 0.02], [1.0, 1.0, 3.0, 5.0, 6.0, 9.0, 3.0, 2.0, 2.0, 5.0], [0.1, 0.5, 0.2, 0.1, 0.25, 0.2, 0.2, 0.1, 0.7, 0.34], 0)           
# print("Stats:")
# for i in range(len(list(out.keys()))):
#     print(list(out.keys())[i], list(out.values())[i])
# MaxHold = 0.15 MaxFloat = 0.02
# displayDictNice(multipleTestRunnerVariable('hello', 0.1, 0.01, 0.05, 0.01, 100), 3)
displayDictNice(multipleTestRunnerVariable("geographically", 1.0,1.0,0.5,0.5,10),3)



start = t.time()
data1 = testerDataFormer("hello", 1.0,1.0,0,0)

# i = Calculation(data1, start, p.User_Profile("Test"), 0)
# make = i.validation(mode='t')

# i = Calculation(data1, start, p.User_Profile("Test"), 0)
# make = i.validation(mode='rnl')


