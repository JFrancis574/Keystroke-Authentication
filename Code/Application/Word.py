from fileinput import filename
import os
from matplotlib.font_manager import json_dump
import numpy as np

class Word:
    
    def __init__(self, wordData = None):
        self.raw = wordData
        self.roundValue = 4
        if wordData != None:
            self.word = self.getWordString()
            self.start = self.raw[0][1]
            self.end = self.raw[-1][2]
        else:
            self.word = None
            self.start = None
            self.end = None
        
    def getWordString(self):
        rawWord = ""
        for x in self.raw:
            rawWord += x[0]
        return rawWord
    
    def KDSWord(self):
        KDSOutput = {}
        multiplier = int(str(1) + self.roundValue*str(0))
        if len(self.raw) != 0:
            for x in range(int(self.raw[0][1]*multiplier), int(self.raw[len(self.raw)-1][2]*multiplier)+1):
                KDSOutput[x/multiplier] = self.KDS(x/multiplier)
        return KDSOutput
    
    def heaviside(self, x1, x2):
        if (x1 > x2):
            return 1
        elif (x1 == x2):
            return 0.5
        else:
            return 0
    
    def KDS(self, time):
        sum = 0
        for i in range(0, len(self.raw)):
            sum += self.heaviside(time, round(self.raw[i][1], self.roundValue)) - self.heaviside(time, round(self.raw[i][2], self.roundValue))
        return sum
    
    def remap_keys(self, mapping):
        return [{'key':k, 'value': v} for k, v in mapping.items()]
    
    def compress(self):
        data = np.array(list(self.KDSforWord.values()))
        keys = np.array(list(self.KDSforWord.keys()))
        startValue = data[0]
        start = keys[0]
        endDict = {}
        for i, j in enumerate(data):
            if j == startValue:
                grouping = (start, keys[i])
            else:
                endDict[grouping] = startValue
                startValue = data[i]
                start = keys[i]
                grouping = (start, keys[i])
            if i == len(data)-1:
                grouping = (start, keys[i])
                endDict[grouping] = startValue
        return self.remap_keys(endDict)