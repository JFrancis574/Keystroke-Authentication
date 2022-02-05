import json
import os.path

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

import Word as w


class Calculation:
    def __init__(self, raw, startTime, pf):
        self.raw = raw
        self.pf = pf
        self.startTime = startTime
        self.chosenAmount = 4
        self.processed = self.process()
        self.pairs = self.rawPairs()
        self.wordsOut = self.words()
        self.noWords = len(self.wordsOut)
        self.chosen = self.wordChooseTemp()
    
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
        currentWord = []
        output = []
        for i in self.pairs:
            if i[0] not in [',','!','space', 'enter', ';',"'",'(',')', ',']:
                if i[0] == 'backspace':
                    if len(currentWord) != 0:
                        currentWord.pop(len(currentWord)-1)
                    else:
                        pass
                elif i[0] ==  self.pairs[len(self.pairs)-1][0]:
                    if len(currentWord) != 0:
                        output.append(w.Word(currentWord))
                    currentWord = []
                else:
                    currentWord.append(i)
            else:
                if len(currentWord) != 0:
                    output.append(w.Word(currentWord))
                currentWord = []
        return output
        
    def wordChoose(self, banding=0):
        wordCount = len(self.self.wordsOutOut)
        if (wordCount == 0 or self.chosenAmount == 0):
            return []
        elif wordCount < self.chosenAmount:
            return []
        elif wordCount == self.chosenAmount:
            return self.self.wordsOutOut
        else:
            diff = self.self.wordsOutOut[-1].end - self.self.wordsOutOut[0].start
            out = []
            wordChooseInterval = diff/self.chosenAmount
            og = diff/self.chosenAmount
            count = 0
            for i in range(0, wordCount):
                if self.self.wordsOutOut[i] == []:
                    pass
                elif wordChooseInterval+banding >= diff:
                    break
                elif self.self.wordsOutOut[i].start <= (wordChooseInterval+banding) and self.self.wordsOutOut[i].end >= (wordChooseInterval+banding):
                    count+=1
                    out.append(self.self.wordsOutOut[i])
                    wordChooseInterval += og + banding
                else:
                    pass
            if len(out) != self.chosenAmount:
                if len(out) == self.chosenAmount-1:
                    y = int(round(len(out)/2, 0))
                    inputWord = self.self.wordsOutOut[y]
                    for x in range(0, len(out)):
                        if inputWord == out[x]:
                            inputWord = self.self.wordsOutOut[y+1]
                    out.append(inputWord)
                    return out
                else:
                    return self.wordChoose(banding+0.1)
            else:
                return out
            
    def wordChooseTemp(self):
        if self.chosenAmount == len(self.wordsOut):
            return self.self.wordsOutOut
        elif self.chosenAmount > len(self.wordsOut):
            return self.wordsOut
        out = []
        out.append(self.wordsOut[0])
        out.append(self.wordsOut[-1])
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
    
    def validation(self):
        distances = {}
        for x in range(0, len(self.chosen)):
            fileName = x.word+'.json'
            if os.path.exists(self.pf.userPath+fileName):
                with open(self.pf.userPath+fileName, 'r') as read_file:
                    dataIn = json.load(read_file)
                read_file.close()
                inInterval = np.array(list(x.KDSWord().values()))
                fromFile = np.array(list(dataIn.values()))
                euclideanDistance, path = fastdtw(fromFile, inInterval, dist=euclidean)
                
                ff_path, ii_path = zip(*path)
                ff_path = np.asarray(ff_path)
                ii_path = np.asarray(ii_path)
                ff_warped = fromFile[ff_path]
                ii_warped = inInterval[ii_path]
        
                correlationCoEfficant = np.corrcoef(ff_warped, ii_warped)[0,1]
                
                distances[x] = [euclideanDistance, correlationCoEfficant]
            # ADD ELSE
        bandingEuc = 10 # The range at which the euc distance is the same user. SUBJECT TO CHANGE
        bandingCorr = 0.5 # # The range at which the Correlation distance is the same user. SUBJECT TO CHANGE
        wordCheck = []
        for j in list(distances.values()):
            # Both are inside the banding = same user
            if j[0] <= bandingEuc and j[1] >= bandingCorr:
                wordCheck.append(True)
            # Correlation is far more important
            elif j[1] >= bandingCorr and j[0] > bandingEuc:
                wordCheck.append(True)
            else:
                wordCheck.append(False)
        
        if False not in wordCheck:
            print("Gucci")
            return True, []
        else:
            print("BAD")
            return False, [(i,j) for i, j in enumerate(wordCheck) if j == False]
            