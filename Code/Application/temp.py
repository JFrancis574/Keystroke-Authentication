import time
import keyboard
import keyboardTest as kt
import Word as w

def record(interval):
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

def wordsObject(pairs):
    currentWord = []
    output = []
    for i in pairs:
        print(i[0])
        if i[0] not in [',','!','space', 'enter', ';',"'",'(',')', ',']:
            if i[0] == 'backspace':
                if len(currentWord) != 0:
                    currentWord.pop(-1)
                else:
                    pass
                    # currentWord = output[-1].raw
                    # output.pop(-1)
                    # currentWord.pop(-1)
            elif i == pairs[-1]:
                currentWord.append(i)
                if len(currentWord) != 0:
                    output.append(w.Word(currentWord))
                currentWord = []
            elif i[0] in ['shift', 'ctrl']:
                pass
            else:
                currentWord.append(i)
        else:
            if currentWord != []:
                output.append(w.Word(currentWord))
            currentWord = []
    return output

print("START")
raw, time = record(60)
print("END")
data = kt.rawPairs(kt.process(time, raw))
for i in data:
    print(i)
words = wordsObject(data)
for x in words:
    print(x.toString())