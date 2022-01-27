#import keyboard
import numpy as np
import matplotlib.pyplot as plt
import json
import pickle
from keyboardTestMac import words, wordChoose, rawPairs, KDSWordByWord
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import os.path

try:
    os.mkdir(os.getcwd()+'/TestData')
except FileExistsError:
    pass


# This is just me typing for an interval, this is meant to mimic
infile = open("60SecondTestData",'rb')  
intervalData = pickle.load(infile)
infile.close()

chosen = wordChoose(words(rawPairs(intervalData)),4)
intervalOut = KDSWordByWord(words(rawPairs(intervalData)),4)
KDSignalWord = KDSWordByWord(chosen,4)

# For every word chosen, select the file from the repository
distances = []
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
        distance, path = fastdtw(fromFile, inInterval, dist=euclidean)
        distances.append(distance)
    else:
        # Currently just store the data
        with open("TestData/"+inFileName, 'w') as write_file:
            json.dump(KDSignalWord[y][1], write_file)
        write_file.close()

        
print(distances)