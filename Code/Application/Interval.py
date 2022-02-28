import getpass
import json
import math
import os.path
import string
import ctypes
import subprocess

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

import Word as w


class Calculation:
    def __init__(self, raw, startTime, pf):
        self.raw = raw
        self.pf = pf
        self.roundInterval = 4
        self.startTime = startTime
        self.chosenAmount = 4
        self.processed = self.process()
        self.pairs = self.rawPairs()
        self.wordsOut = self.words()
        self.noWords = len(self.wordsOut)
        self.chosen = self.choose()
    
    def process(self):
        if len(self.raw) == 0:
            return []
        rawKeys = []
        count = 0
        for record in self.raw:
            count += 1
            rawKeys.append([record.name, (record.time - self.startTime), record.event_type])
        return rawKeys
    
    def rawPairs(self):
        pairsArray = []
        for i in range(len(self.processed)):
            try:
                if (self.processed[i][2] == 'down' and self.processed[i+1][2] == 'up' and self.processed[i][0].lower() == self.processed[i+1][0].lower()):
                    pairsArray.append([self.processed[i][0], self.processed[i][1], self.processed[i+1][1]])
                else:
                    for x in range(i, len(self.processed)):
                        if (self.processed[x][0].lower() == self.processed[i][0].lower() and self.processed[x][2] == 'up' and self.processed[i][2] == 'down'):
                            pairsArray.append([self.processed[i][0], self.processed[i][1], self.processed[x][1]])
                            break        
            except IndexError:
                pass
        return pairsArray
    
    def words(self):
        bannedPunc = ['space', 'enter','play/pause media','alttab', 'eqdown', 'right', 'left', 'up', 'down', 'tab','alt', 'shift', 'ctrl']
        currentWord = []
        output = []
        for j, i in enumerate(self.pairs):
            if i[0] not in bannedPunc and i[0] not in string.punctuation:
                if i[0] == 'backspace':
                    if len(currentWord) != 0:
                        currentWord.pop(-1)
                        if i == self.pairs[-1]:
                            output.append(w.Word(currentWord))
                            currentWord = []
                    else:
                        if len(output) != 0:
                            currentWord = output.pop(-1).raw
                elif i == self.pairs[-1]:
                    currentWord.append(i)
                    if len(currentWord) != 0:
                        output.append(w.Word(currentWord))
                    currentWord = []
                else:
                    currentWord.append(i)
            else:
                if i[0] in ['space', '.', 'enter', ',',':',';']:
                    if len(currentWord) != 0:
                        output.append(w.Word(currentWord))
                    currentWord = []
                elif i[0] == "'" or i[0] == '-':
                    if len(currentWord) == 0:
                        pass
                    else:
                        try:
                            if currentWord[-1][0].isalpha() and self.pairs[j+1][0].isalpha():
                                currentWord.append(i)
                            else:
                                output.append(w.Word(currentWord))
                                currentWord = []
                        except IndexError:
                            output.append(w.Word(currentWord))
                            currentWord = []
                else:
                    pass
        return output
        
    def choose(self):
        out = []
        if len(self.wordsOut) <= self.chosenAmount:
            return self.wordsOut
        elif self.chosenAmount == 1:
            return [self.wordsOut[len(self.wordsOut//2)]]
        
        tempWords = self.wordsOut
        while True:
            if len(out) == self.chosenAmount or len(tempWords) == 1:
                return out
            mid = len(tempWords)//2
            out.append(tempWords.pop(mid))
            
    def wordChooseTemp(self):
        if self.chosenAmount == len(self.wordsOut):
            return self.wordsOut
        elif self.chosenAmount > len(self.wordsOut):
            return self.wordsOut
        out = [self.wordsOut[0], self.wordsOut[-1]]
        self.wordsOut.pop(0)
        self.wordsOut.pop(-1)

        if len(out) != self.chosenAmount:
            chosenAmount = self.chosenAmount-2
            og = int(len(self.wordsOut)/chosenAmount)
            diff = int(len(self.wordsOut)/chosenAmount)
            for x in range(0, len(self.wordsOut)):
                if len(out) == self.chosenAmount:
                    break
                if x == diff:
                    out.append(self.wordsOut[x])
                    diff += og
        return out
    
    def validation(self, mode='r'):
        # r = real t = test
        distances = {}
        if mode == 'r':
            for x in range(0, len(self.chosen)):
                fileName = self.chosen[x].word+'.json'
                if os.path.exists(self.pf.userPath+fileName):
                    # Loading in the data from the word files
                    with open(self.pf.userPath+fileName, 'r') as read_file:
                        dataIn = self.decompress(json.load(read_file))
                    read_file.close()
                    
                    # Beautifying and forming the correct data
                    inInterval = np.array(list(self.chosen[x].KDSWord().values()))
                    fromFile = np.array(list(dataIn.values()))
                    
                    # Euciladitan and fastdtw
                    euclideanDistance, path = fastdtw(fromFile, inInterval, dist=euclidean)
                    
                    ff_path, ii_path = zip(*path)
                    ff_path = np.asarray(ff_path)
                    ii_path = np.asarray(ii_path)
                    ff_warped = fromFile[ff_path]
                    ii_warped = inInterval[ii_path]
            
                    
                    # CorrelationCoefficant
                    # correlationCoEfficant = np.corrcoef(ff_warped, ii_warped)[0,1]
                    cov = 0
                    XSum = 0
                    YSum = 0
                    for i in range(len(ff_warped)):
                        cov += (ff_warped[i] - np.mean(ff_warped))*(ii_warped[i] - np.mean(ii_warped))
                        XSum += math.pow(ff_warped[i]-np.mean(ff_warped), 2)
                        YSum += math.pow(ii_warped[i]-np.mean(ii_warped), 2)   
                    
                    correlationCoEfficant = cov/((math.sqrt(XSum)*(math.sqrt(YSum))))
                    distances[x] = [euclideanDistance, correlationCoEfficant]
                else:
                    distances[x] = [None, None]
                
            bandingEuc = 1000 # The range at which the euc distance is the same user. SUBJECT TO CHANGE
            bandingCorr = 0.99 # The range at which the Correlation distance is the same user. SUBJECT TO CHANGE
            wordCheck = []
            for j in list(distances.values()):
                print("j: ", j)
                if j[0] == None:
                    wordCheck.append(None)
                # Both are inside the banding = same user
                elif j[0] <= bandingEuc and j[1] >= bandingCorr:
                    wordCheck.append(True)
                # Correlation is far more important
                elif j[1] >= bandingCorr and j[0] > bandingEuc:
                    wordCheck.append(True)
                else:
                    wordCheck.append(False)
        
            print(wordCheck)
            if len(wordCheck) != 1:
                if False not in wordCheck and None not in wordCheck:
                    return True, []
                elif False not in wordCheck and None in wordCheck:
                    self.update([i for i, j  in enumerate(wordCheck) if j == None])
                    return True, []
                elif False in wordCheck and None in wordCheck:
                    # Code to lock pc
                    self.lockPc()
                    # The user then re-authenticates
                    # Check if user re-authenticates successfully
                    while True:
                        if self.checkLocked():
                            break
                        # If the same user,
                    if getpass.getuser() == self.pf.user:
                        self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                        return True, []
                    else:
                        # Otherwise, set up a new profile
                        return 'New', []
                else:
                    return False, [(i,j) for i, j in enumerate(wordCheck) if j == False]
            else:
                if True in wordCheck:
                    return True, []
                elif False in wordCheck:
                    self.lockPc()
                    while True:
                        if self.checkLocked():
                            break
                        # If the same user,
                    if getpass.getuser() == self.pf.user:
                        self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                        return True, []
                    else:
                        # Otherwise, set up a new profile
                        return 'New', []
                elif None in wordCheck:
                    self.lockPc()
                    while True:
                        if self.checkLocked():
                            break
                        # If the same user,
                    if getpass.getuser() == self.pf.user:
                        self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                        return True, []
                    else:
                        # Otherwise, set up a new profile
                        return 'New', []
                        
        else:
            # Current reg system, just generate and save KDS for every word
            # TEMP  - WILL NEED IMPROV
            for x in range(0, len(self.wordsOut)):
                fileName = self.wordsOut[x].word+'.json'
                Kds = self.wordsOut[x].compress()
                print(self.pf.userPath)
                if os.path.exists(self.pf.userPath+fileName):
                    pass
                else:
                    with open(self.pf.userPath+fileName, 'w') as write_file:
                        json.dump(Kds, write_file)
                    write_file.close()
            return True, []
        
    def decompress(self, data):
        outDict = {}
        multiplier = int(str(1) + self.roundInterval*str(0))
        multiplierPlus1 = int(str('11') + str(int(self.roundInterval-1)*'0'))
        for x in data:
            startTime = list(x.values())[0][0]
            endTime = list(x.values())[0][1]
            value = list(x.values())[1]
            for x in range(int(startTime*multiplier), int(endTime*multiplierPlus1)+1):
                outDict[x/multiplier] = value
        return outDict
    
    def __str__(self):
        out = "Words: "
        for x in self.wordsOut:
            out += "\n"+x.toString()
        out += "\nChosen: "
        for i in self.chosen:
            out += "\n"+i.toString()
        return out
    
    def update(self, indexes):
        intruderWords = [self.chosen[indexes[i]] for i in range(len(indexes))]
        for x in intruderWords:
            fileName = x.word+'.json'
            Kds = x.compress()
            with open(self.pf.userPath+fileName, 'w') as write_file:
                json.dump(Kds, write_file)
            write_file.close()
            
    def lockPc(self):
        cmd='rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)
            
    def checkLocked(self):
        user32 = ctypes.windll.User32
        if (user32.GetForegroundWindow() % 10 != 0):
            return False
        else:
            return True