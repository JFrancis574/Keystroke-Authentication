from fileinput import filename
import pickle
import matplotlib.pyplot as plt
import json
import os.path
from fastdtw import fastdtw
import numpy as np
from scipy.spatial.distance import euclidean

from numpy import fromfile, int0
from keyboardTestMac import words, rawPairs, KDSWordByWord, wordChoose

try:
    os.mkdir(os.getcwd()+'/TestData')
except FileExistsError:
    pass

infile = open("60SecondTestData",'rb')  
intervalData = pickle.load(infile)
infile.close()

infile = open("Hello1",'rb')
singleWord = pickle.load(infile)
infile.close()

intervalOut = KDSWordByWord(words(rawPairs(intervalData)),4)
singleWordOut = KDSWordByWord(words(rawPairs(singleWord)),4)

with open("TestData/JSONTestFile.json", 'w') as write_file:
    json.dump(singleWordOut, write_file)

write_file.close()

with open("TestData/JSONTestFile.json", "r") as read_file:
    data = json.load(read_file)

for i in range(0, len(intervalOut)):
    word = ""
    for x in words(rawPairs(intervalData))[i]:
        word+= x[0]
    fileName = word +'.json'
    with open("TestData/"+fileName, 'w') as write_file:
        json.dump(intervalOut[i][1], write_file)
    write_file.close()

chosen = wordChoose(words(rawPairs(intervalData)),4)
KDSignalWord = KDSWordByWord(chosen,4)

for y in range(0, len(KDSignalWord)):
    word = ""
    for x in chosen[y]:
        word+=x[0]
    inFileName = word+'.json'
    if os.path.exists(os.getcwd()+'/TestData/'+inFileName):
        with open("TestData/"+inFileName, 'r') as read_file:
            dataIn = json.load(read_file)
        read_file.close()
        inInterval = np.array(list(KDSignalWord[y][1].values()))
        fromFile = np.array(list(dataIn.values()))
        print(word)
        print(fromFile[-1], inInterval[-1])
        print(len(fromFile), len(inInterval))
        print(fromFile == inInterval)
        print(np.array_equiv(inInterval, fromFile))
        
        distance, path = fastdtw(fromFile, inInterval, dist=euclidean)
        print(distance)
        

