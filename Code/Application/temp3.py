from black import out
import Word as w
import keyboardTest as kt
import Interval as i
import pickle

def wordChoose(words, amountofWords, banding=0):
    wordCount = len(words)
    if (wordCount == 0 or amountofWords == 0):
        return []
    elif wordCount < amountofWords:
        return []
    elif wordCount == amountofWords:
        return words
    else:
        diff = words[-1].end - words[0].start
        out = []
        wordChooseInterval = diff/amountofWords
        og = diff/amountofWords
        count = 0
        for i in range(0, wordCount):
            if words[i] == []:
                pass
            elif wordChooseInterval+banding >= diff:
                break
            elif words[i].start <= (wordChooseInterval+banding) and words[i].end >= (wordChooseInterval+banding):
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
                return wordChoose(words, amountofWords, banding+0.1)
        else:
            return out



def wordsObject(pairs):
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
                output.append(w.Word(currentWord))
                currentWord = []
            else:
                currentWord.append(i)
        else:
            output.append(w.Word(currentWord))
            currentWord = []
    return output

infile = open("C:/Users/jackf/Documents/FinalYearProject/Code/Test Code/Data/Pickles/"+"HoeyTestData",'rb')  
intervalData = pickle.load(infile)
infile.close()


data, start = kt.record(10)
# print(data)
inter = i.Calculation(data, start)
# print(inter.wordsOut)

# for x in wordsObject(kt.rawPairs(intervalData)):
#     print(x.raw)
    
# print(len(wordChoose(wordsObject(kt.rawPairs(intervalData)),4)))