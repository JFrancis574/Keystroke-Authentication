#import keyboard
import json
import os.path
import pickle

import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

from keyboardTestMac import KDSWordByWord, rawPairs, wordChoose, words
# from keyboardTest import recordReg
import setup as st

dConn = st.DBCreation("keyStorage.db")
regWords = ""

def register():
    while True:
        Uname = input("USERNAME: ")
        Password = input("PASSWORD: ")
        if dConn.uNameExists():
            print("Uname taken")
        else:
            dConn.insertLoginInfoEnc(Uname, Password)
            break
    while True:
        print("Please type the words below:\n")
        print(regWords+'\n')
        regData = words(recordReg(regWords[-1]))
        if regData != False:
            storeWordData()
            
def storeWordData(username, words):
    DataPath = st.getUserDataPath(username)
    Kds = KDSWordByWord(words)
    for i in range(0, len(intervalOut)):
        word = ""
        for x in words(rawPairs(intervalData))[i]:
            word+= x[0]
        fileName = word +'.json'
        if os.path.exists(DataPath+fileName):
            pass
        else:
            with open(DataPath+fileName, 'w') as write_file:
                json.dump(intervalOut[i][1], write_file)
            write_file.close()
        
        
def testData(fileName):
    # This is just me typing for an interval, this is meant to mimic
    infile = open(os.getcwd()+"/Data/Pickles/"+fileName,'rb')  
    intervalData = pickle.load(infile)
    infile.close()

    chosen = wordChoose(words(rawPairs(intervalData)),4)
    KDSignalWord = KDSWordByWord(chosen,4)
    return chosen,KDSignalWord

# For every word chosen, select the file from the repository
# mode = t (test), g = (genuine)
def distanceCalc(chosen, KDSignalWord, mode="t"):
    if mode == "t":
        dataPath = st.getUserTestDataPath()
    else:
        dataPath = st.getUserDataPath()
    distances = {}
    for y in range(0, len(KDSignalWord)):
        word = ""
        for x in chosen[y]:
            word+=x[0]
        inFileName = word+'.json'
        if os.path.exists(os.getcwd()+'/Data/WordData/'+inFileName):
            with open(os.getcwd()+"/Data/WordData/"+inFileName, 'r') as read_file:
                dataIn = json.load(read_file)
            read_file.close()
            inInterval = np.array(list(KDSignalWord[y][1].values()))
            fromFile = np.array(list(dataIn.values()))
            euclideanDistance, path = fastdtw(fromFile, inInterval, dist=euclidean)
            
            ff_path, ii_path = zip(*path)
            ff_path = np.asarray(ff_path)
            ii_path = np.asarray(ii_path)
            ff_warped = fromFile[ff_path]
            ii_warped = inInterval[ii_path]
    
            correlationCoEfficant = np.corrcoef(ff_warped, ii_warped)[0,1]
            
            distances[y] = [euclideanDistance, correlationCoEfficant]
            
        else:
            pass
        # Currently just store the data
            # with open(os.getcwd()+"/Data/WordData/"+inFileName, 'w') as write_file:
            #      json.dump(KDSignalWord[y][1], write_file)
            # write_file.close()
    return distances

def validation(distances):
    bandingEuc = 10 # The range at which the euc distance is the same user. SUBJECT TO CHANGE
    bandingCorr = 0.5 # # The range at which the Correlation distance is the same user. SUBJECT TO CHANGE
    wordCheck = []
    for i, j in enumerate(distances.values()):
        print(i, j)
        # Both are inside the banding = same user
        if j[0] <= bandingEuc and j[1] >= bandingCorr:
            wordCheck.append(True)
        # Correlation is far more important
        elif j[1] >= bandingCorr and j[0] > bandingEuc:
            wordCheck.append(True)
        else:
            wordCheck.append(False)
    return wordCheck

chosen, KDSignalWord = testData("HoeyTestData")
print(chosen[0])
distances = distanceCalc(chosen, KDSignalWord)

print(distances)

print(validation(distances))
