import keyboardTest as kt



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