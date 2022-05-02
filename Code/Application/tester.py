# JSON implementation inside Python Standard Lib
# https://docs.python.org/3/library/json.html
import json

# Random implementation inside Python Standard Lib
# https://docs.python.org/3/library/random.html
import random

# Used to generate the graph, implementation by The Matplotlib Development team
# https://matplotlib.org
from matplotlib import pyplot as plt

# OS implementation inside Python Standard Lib
# https://docs.python.org/3/library/os.html
import os

# time implementation inside Python Standard Lib
# https://docs.python.org/3/library/time.html
import time as t

# timeit implementation inside Python Standard Lib
# https://docs.python.org/3/library/timeit.html
import timeit

# Used to generate conf matrix, implementation by Scikit
# https://scikit-learn.org/stable/
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# NumPy implementation by NumPy
# https://numpy.org/
# Last updated: 02/05/2022
import numpy as np

# sys implementation in Python Standard lib
# https://docs.python.org/3/library/sys.html
from sys import platform

from Training import Training
import user_profile as p
from Interval import Calculation

if platform == 'darwin':
    import keyboardEvent as k
else:
    import keyboard as k

def testerDataFormer(string, holdTime, floatTime, file=0, variable=0):
    """Used to form test data

    Args:
        string (string): The word to "type" out
        holdTime (float or array): The holdtime if array iterates through
        floatTime (float or array): The floattime if array iterates through
        file (int, optional): If to load in from file. Defaults to 0.
        variable (int, optional): If to variablise the data. Defaults to 0.

    Returns:
        KeyboardEvent: KeyboardEvent rep of input
    """
    output = []
    # if file
    if file == 0:
        data = string
    else:
        if os.path.exists(os.getcwd()+string):
            data = open(string, 'r')
        else:
            return
    
    
    # Check what types the data hold
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
    """Used to run multiple tests

    Args:
        Teststring (string): The string to run the tests on
        iterations (int): How many tests
        imposterCount (int): How many are imposters
        genuineHoldData (array, float): The array of genuine hold data
        genuineFloatData (array, float): The array of genuine float data 
        imposterHoldData (array, float): The array of imposter hold data 
        imposterFloatData (array, float): The array of imposter float data 
        benchmark (int, optional): If no benchmark exists. Defaults to 0.

    Returns:
        dict: The resultant scores
    """
    if iterations == 0 or Teststring == "":
        return
    pf = p.Profile('Test')
    
    # Creates the benchmark
    if benchmark == 0:
         # No benchmark exists
        print("Creating Benchmark")
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


def testDataFormerInter(data, holdTime, floatTime, r=0):
    """Uses interleaving

    Args:
        data (string): The test data to generate
        holdTime (float): The holdtime
        floatTime (float): The floattime
        r (int, optional): If it is random or not. Defaults to 0.

    Returns:
        array of KeyboardEvent: The resulting data
    """
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
        
    
def displayDictNice(dict, roundValue):
    """Simply prints the dict nicely

    Args:
        dict (dict): The dict to be displayed nicely
        roundValue (_type_): _description_
    """
    if len(list(dict.keys())) == 0:
        return
    print("TNO: HT: FT: D:")
    values = list(dict.values())
    for i in range(len(list(dict.keys()))):
        print(i, round(values[i][0], roundValue), round(values[i][1], roundValue), values[i][2])
                
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
    
    
def record(interval, words, expected):
    """Recording keystrokes function

    Args:
        interval (float): How long to record for

    Returns:
        keystroke data: Comprised of a dictionary
        starttime: Comprised of the starttime of the data
    """
    recorded = []
    # Uses pythons builtin time library
    # https://docs.python.org/3/library/time.html
    startTime = t.time()

    print("Recording")
    print("Write the following words")
    print(words)
    print(expected)
    # Uses the keyboard lib to unhook and hook the data
    # Implementation by Broppeh
    # https://github.com/boppreh/keyboard
    keyBoardHook = k.hook(recorded.append)
    t.sleep(interval)
    print("Stopping")
    k.unhook(keyBoardHook)
    return recorded, startTime

def process(data, start):
    """
    Converts the raw keystroke data into a pair consisting of both the up and down actions.

    Returns:
        2D array: 2 dimensional array consisting of a seperate array for each key action. Converts the time into one that can actually be used.
    """
    if len(data) == 0:
        return []
    rawKeys = []
    for record in data:
        rawKeys.append([record.name, (record.time - start), record.event_type])
    return rawKeys


def test2(all=False):
    print(2)
    stop = False
    interval = 60
    tests = 4
    expected = [[True, True, True, True], [True, True, False, True], [False, False, False, False], [True, False, True, False]]
    words = ["Hello", "google", "words", "geographically"]
    outputDist = {}
    outputDec = {}
    prof = p.User_Profile("Test")
    if len(os.listdir(prof.getKeyboardPath())) == 0:
        print("Benchmark")
        data, start = record(interval, words, [])
        train = Training(data, start, prof, 1, None, 0)
        print("Benchmark Done")
    return
        
    i = 3
    while i < tests:
        data, start = record(interval, words, expected[i])
        inter = Calculation(data, start, prof, 1, lambda: stop)
        distances, decision = inter.validation(mode='t')
        print(decision)
        if decision == expected[i] or all == True:
            outputDist[i] = distances
            outputDec[i] = decision
            filename = "Words"+str(i)+'.json'
            data = process(data, start)
            with open(filename, 'w') as write:
                json.dump(data, write)
            i += 1
        else:
            print("Doesn't match")
            
def loadInJson(data):
    with open(data, 'r') as read:
        rawData = json.load(read)
    return rawData

test2(all=True)

def confMatrix():
    files = ["Words0.json","Words1.json","Words2.json","Words3.json"]
    stop = False
    prof = p.User_Profile("Test")
    allDec = []
    expected = [True, True, True, True, True, True, False, True, False, False, False, False, True, False, True, False]
    for x in files:
        inter = Calculation([], [], prof, 1, lambda: stop)
        inter.processed = loadInJson(x)
        inter.pairs = inter.rawPairs()
        inter.wordsOut, inter.semantics = inter.words()
        inter.noWords = len(inter.wordsOut)
        inter.chosen = inter.choose()
        startTime = t.time()
        _, dec = inter.validation(mode='t')
        print(t.time() - startTime)
        allDec.append(dec)
    allDec = np.asarray(allDec)
    final = allDec.ravel()
    cm = confusion_matrix(expected, final)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.show()
    
confMatrix()




    






