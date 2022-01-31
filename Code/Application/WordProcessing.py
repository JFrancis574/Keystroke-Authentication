import time
import keyboard
import numpy as np

class wordProcessing:
    
    def __init__(self, interval, amountofWords, profile):
        self.uName
        self.interval = interval
        self.roundInterval = 4
        self.raw, self.start = self.record(interval)
        self.process = self.process(self.raw)
        self.pairs = self.rawPairs(self.raw)
        self.wordOut = self.words(self.pairs)
        self.KDSWord = self.KDSWordByWord(self.wordOut)
        self.chosen = self.wordChoose(self.KDSWord, amountofWords)
        
    def record(self, interval):
        recorded = []
        startTime = time.time()
        keyBoardHook = keyboard.hook(recorded.append)
        time.sleep(interval)
        keyboard.unhook(keyBoardHook)
        return recorded , startTime
    
    def process(self, keys):
        if len(keys) == 0:
            return []
        rawKeys = []
        count = 0
        for record in keys:
            count += 1
            rawKeys.append([record.name, (record.time - self.start), record.event_type])
        return rawKeys
    
    def rawPairs(self, rawKeys):
        pairsArray = []
        for i in range(len(rawKeys)):
            try:
                if (rawKeys[i][2] == 'down' and rawKeys[i+1][2] == 'up' and rawKeys[i][0].lower() == rawKeys[i+1][0].lower()):
                    pairsArray.append([rawKeys[i][0], rawKeys[i][1], rawKeys[i+1][1]])
                else:
                    for x in range(i, len(rawKeys)):
                        if (rawKeys[x][0].lower() == rawKeys[i][0].lower() and rawKeys[x][2] == 'up' and rawKeys[i][2] == 'down'):
                            pairsArray.append([rawKeys[i][0], rawKeys[i][1], rawKeys[x][1]])
                            break        
            except IndexError:
                pass;
        return pairsArray
    
    def words(self, pairs):
        currentWord = []
        output = []
        for i in pairs:
            if i[0] not in [',','!','space', 'enter', ';',"'",'(',')', ',']:
                if i[0] == 'backspace':
                    if len(currentWord) != 0:
                        currentWord.pop(len(currentWord)-1)
                    else:
                        pass
                elif i[0] == pairs[len(pairs)-1][0]:
                    output.append(currentWord)
                    currentWord = []
                else:
                    currentWord.append(i)
            else:
                output.append(currentWord)
                currentWord = []
        return output
    
    def heaviside(self, x1, x2):
        if (x1 > x2):
            return 1
        elif (x1 == x2):
            return 0.5
        else:
            return 0

    # KDS function
    def KDS(self, time, keysArray):
        sum = 0
        for i in range(0, len(keysArray)):
            sum += self.heaviside(time, round(keysArray[i][1], self.roundInterval)) - self.heaviside(time, round(keysArray[i][2], self.roundInterval))
        return sum

    def KDSWordByWord(self, wordsOut):
        KDSOutput = {}
        WordByWord = []
        multiplier = int(str(1) + self.roundInterval*str(0))
        for i in range(0, len(wordsOut)):
            if len(wordsOut[i]) != 0:
                for x in range(int(wordsOut[i][0][1]*multiplier), int(wordsOut[i][len(wordsOut[i])-1][2]*multiplier)+1):
                    KDSOutput[x/multiplier] = self.KDS(x/multiplier, wordsOut[i], self.roundInterval) 
                WordByWord.append([i,KDSOutput])
                KDSOutput = {}
        return WordByWord
    
    def wordChoose(self, words, amountofWords, banding=0):
        wordCount = len(words)
        if (wordCount == 0 or amountofWords == 0):
            return []
        elif wordCount < amountofWords:
            return []
        elif wordCount == amountofWords:
            return words
        else:
            diff = words[-1][-1][2] - words[0][0][1]
            out = []
            wordChooseInterval = diff/amountofWords
            og = diff/amountofWords
            count = 0
            for i in range(0, wordCount):
                if wordChooseInterval+banding >= diff:
                    break
                elif words[i][0][1] <= (wordChooseInterval+banding) and words[i][-1][2] >= (wordChooseInterval+banding):
                    count+=1
                    out.append(words[i])
                    wordChooseInterval += og + banding
                else:
                    pass
            if len(out) != amountofWords:
                if len(out) == amountofWords-1:
                    y = int(round(len(out)/2, 0))
                    inputWord = words[y]
                    for x in range(0, len(out)):
                        if inputWord == out[x]:
                            inputWord = words[y+1]
                    out.append(inputWord)
                    return out
                else:
                    return self.wordChoose(words, amountofWords, banding+0.1)
            else:
                return out
            
    def remap_keys(self, mapping):
        return [{'key':k, 'value': v} for k, v in mapping.items()]
    
    def compress(self, dataIn):
        data = np.array(list(dataIn.values()))
        keys = np.array(list(dataIn.keys()))
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
        
    def unCompress(self, data):
        outDict = {}
        multiplier = int(str(1) + self.interval*str(0))
        multiplierPlus1 = int(str(11) + self.interval-1*str(0))
        for x in data:
            print(x)
            startTime = list(x.values())[0][0]
            endTime = list(x.values())[0][1]
            value = list(x.values())[1]
            print(startTime, endTime, value)
            for x in range(int(startTime*multiplier), int(endTime*multiplierPlus1)+1):
                outDict[x/multiplier] = value
        return outDict