import Word as w

class Calculation:
    def __init__(self, raw, startTime):
        self.raw = raw
        self.startTime = startTime
        self.chosenAmount = 4
        self.processed = self.process()
        self.pairs = self.rawPairs()
        # print("CALC")
        # print(self.pairs)
        self.wordsOut = self.words()
        self.noWords = len(self.wordsOut)
        self.chosen = self.wordChoose()
    
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
                    print(currentWord)
                    output.append(w.Word(currentWord))
                    currentWord = []
                else:
                    currentWord.append(i)
            else:
                print(currentWord)
                output.append(w.Word(currentWord))
                currentWord = []
        print(output)
        return output
        
    def wordChoose(self, banding=0):
        wordCount = len(self.wordsOut)
        if (wordCount == 0 or self.chosenAmount == 0):
            return []
        elif wordCount < self.chosenAmount:
            return []
        elif wordCount == self.chosenAmount:
            return self.wordsOut
        else:
            diff = self.wordsOut[-1].end - self.wordsOut[0].start
            out = []
            wordChooseInterval = diff/self.chosenAmount
            og = diff/self.chosenAmount
            count = 0
            for i in range(0, wordCount):
                if self.wordsOut[i] == []:
                    pass
                elif wordChooseInterval+banding >= diff:
                    break
                elif self.wordsOut[i].start <= (wordChooseInterval+banding) and self.wordsOut[i].end >= (wordChooseInterval+banding):
                    count+=1
                    out.append(self.wordsOut[i])
                    wordChooseInterval += og + banding
                else:
                    pass
            if len(out) != self.chosenAmount:
                if len(out) == self.chosenAmount-1:
                    y = int(round(len(out)/2, 0))
                    inputWord = self.wordsOut[y]
                    for x in range(0, len(out)):
                        if inputWord == out[x]:
                            inputWord = self.wordsOut[y+1]
                    out.append(inputWord)
                    return out
                else:
                    return self.wordChoose(banding+0.1)
            else:
                return out
    
    