from cProfile import label
import json
import random

from matplotlib import pyplot as plt
import numpy as np
from Training import Training
import user_profile as p
import os
import time as t
from Interval import Calculation
import timeit
from fastdtw import fastdtw

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
# displayDictNice(multipleTestRunnerVariable("geographically", 1.0,1.0,0.5,0.5,10),3)



# start = t.time()
# data1 = testerDataFormer("hello", 1.0,1.0,0,0)

# # i = Calculation(data1, start, p.User_Profile("Test"), 0)
# # make = i.validation(mode='t')

# # i = Calculation(data1, start, p.User_Profile("Test"), 0)
# # make = i.validation(mode='rnl')

# start = t.time()
# data1 = testerDataFormer("hello", 1.0, 1.0, 0,0)
# start2 = t.time()
# data2 = testerDataFormer("hello", 1.5,1.5,0,0)

# inter1 = Calculation(data1, start, p.User_Profile("Test"), 0)
# data1KDS = inter1.chosen[0].KDSWord()
# inter2 = Calculation(data2, start2, p.User_Profile("Test"), 0)
# data2KDS = inter2.chosen[0].KDSWord()

# print(data1KDS)
# print(list(data1KDS.keys()))


# # KDS1 = {0.1 : 1, 0.2 : 2, 0.3 : 3, 0.4 : 3, 0.5 : 2, 0.6 : 2, 0.7 : 1, 0.8 : 0, 0.9 : 1}
# # KDS2 = {0.1 : 1, 0.2 : 2, 0.3 : 2, 0.4 : 2, 0.5 : 1, 0.6 : 0.5, 0.7 : 2, 0.8 : 2}

# KDS1 = data1KDS
# KDS2 = data2KDS

# plt.subplot(2,1,1)
# plt.plot(list(KDS1.keys()), list(KDS1.values()))
# plt.title("KDS signal generated for the word hello")
# plt.xlabel("Time (Seconds)")
# plt.ylabel("KDS")
# plt.show()

# # plt.subplot(2,1,2)
# plt.plot(list(KDS2.keys()), list(KDS2.values()))
# plt.title("KDS signal generated for the word hello")
# plt.xlabel("Time (Seconds)")
# plt.ylabel("KDS")
# plt.show()

# plt.plot(list(KDS1.keys()), list(KDS1.values()), label="First user")
# plt.plot(list(KDS2.keys()), list(KDS2.values()), label="Second user")
# plt.legend(loc="upper left")
# plt.title("KDS signal generated for the word hello")
# plt.xlabel("Time (Seconds)")
# plt.ylabel("KDS")
# plt.show()

# x = list(KDS1.values())
# y = list(KDS2.values())


# distance, path = fastdtw(x, y, dist=None)

# x_path, y_path = zip(*path)
# x_path = np.asarray(x_path)
# y_path = np.asarray(y_path)
# x_warped = x[x_path]
# y_warped = y[y_path]


# plt.plot(list(KDS1.keys()), x_warped)
# plt.title("KDS signal 1 after going through Dynamic Time Warping")
# plt.xlabel("Time (Seconds)")
# plt.ylabel("KDS")
# plt.show()

# plt.plot(list(KDS2.keys()), y_warped)
# plt.title("KDS signal 1 after going through Dynamic Time Warping")
# plt.xlabel("Time (Seconds)")
# plt.ylabel("KDS")
# plt.show()
    


def test1():
    print(1)
    start = 0.1
    end = 1.0
    ref = 0.5
    floatTime = 0.1
    decisions = {}
    euc = {}
    corr = {}
    startTime = t.time()
    referenceData = testerDataFormer("geographically", ref , floatTime, 0,0)
    prof = p.User_Profile("Test")
    inter = Training(referenceData, startTime, prof, 0,0)
    x = start
    while x <= end:
        x = round(x, 1)
        startTime = t.time()
        data = testerDataFormer("geographically", x, floatTime, 0,0)
        distance, output = Calculation(data, startTime, prof,0).validation(mode='t')
        euc[x] = list(distance.values())[0][0]
        corr[x] = list(distance.values())[0][1]
        decisions[x] = output
        x += 0.1

    # Euc Graph
    x = list(euc.keys())
    y = list(euc.values())

    plt.plot(x,y)
    plt.title("Euclidean Distance")
    plt.xlabel("HoldTime")
    plt.ylabel("Euc Score")
    plt.show()

    # Corr Graph
    x = list(corr.keys())
    y = list(corr.values())

    plt.plot(x, y)
    plt.title("2D Correlation Score")
    plt.xlabel("HoldTime")
    plt.ylabel("Correlation Score")
    plt.show()

    # Decisions
    x = list(decisions.keys())
    y = list(decisions.values())

    plt.plot(x, y)
    plt.title("Decisions")
    plt.xlabel("HoldTime")
    plt.ylabel("Decision")
    plt.show()


def testDataFormerInter(data, holdTime, floatTime, r=0):
    time = t.time()
    output = []
    if r == 1:
        x = 0
        while x < len(data):
            if random.choice([0,1]) == 0 or x == len(data)-1:
                output.append(k.KeyboardEvent('down', 99, name=data[x], time=time))
                time+= holdTime
                output.append(k.KeyboardEvent('up', 99, name=data[x], time=time))
                time += floatTime
                x += 1
            else:
                output.append(k.KeyboardEvent('down', 99, name=data[x], time=time))
                output.append(k.KeyboardEvent('down', 99, name=data[x+1], time=time))
                time+= holdTime
                output.append(k.KeyboardEvent('up', 99, name=data[x+1], time=time))
                output.append(k.KeyboardEvent('up', 99, name=data[x], time=time))
                time += floatTime
                x += 2
    else:
        x = 0
        while x < len(data):
            if x % 2 == 0 or x == len(data)-1:
                output.append(k.KeyboardEvent('down', 99, name=data[x], time=time))
                time+= holdTime
                output.append(k.KeyboardEvent('up', 99, name=data[x], time=time))
                time += floatTime
                x += 1
            else:
                output.append(k.KeyboardEvent('down', 99, name=data[x], time=time))
                output.append(k.KeyboardEvent('down', 99, name=data[x+1], time=time))
                time+= holdTime
                output.append(k.KeyboardEvent('up', 99, name=data[x+1], time=time))
                output.append(k.KeyboardEvent('up', 99, name=data[x], time=time))
                time += floatTime
                x += 2

    return output

def test2():
    print(2)
    start = 0.1
    end = 1.0
    ref = 0.5
    floatTime = 0.1
    decisions = {}
    euc = {}
    corr = {}
    startTime = t.time()
    referenceData = testDataFormerInter("geographically", ref , floatTime, r=0)
    prof = p.User_Profile("Test")
    inter = Training(referenceData, startTime, prof, 0,0)
    x = start
    while x <= end:
        x = round(x, 1)
        startTime = t.time()
        data = testDataFormerInter("geographically", x, floatTime, r=0)
        distance, output = Calculation(data, startTime, prof,0).validation(mode='t')
        euc[x] = list(distance.values())[0][0]
        corr[x] = list(distance.values())[0][1]
        decisions[x] = output
        x += 0.1


    # Euc Graph
    x = list(euc.keys())
    y = list(euc.values())

    plt.plot(x,y)
    plt.title("Euclidean Distance")
    plt.xlabel("HoldTime")
    plt.ylabel("Euc Score")
    plt.show()

    # Corr Graph
    x = list(corr.keys())
    y = list(corr.values())

    plt.plot(x, y)
    plt.title("2D Correlation Score")
    plt.xlabel("HoldTime")
    plt.ylabel("Correlation Score")
    plt.show()

    # Decisions
    x = list(decisions.keys())
    y = list(decisions.values())

    plt.plot(x, y)
    plt.title("Decisions")
    plt.xlabel("HoldTime")
    plt.ylabel("Decision")
    plt.show()

test2()



    






