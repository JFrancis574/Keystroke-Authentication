import Interval as inter
import profile as pf
import time
import keyboard

interval = 10

Upf = pf.Profile("Jack", "Pass")
print(Upf.userPath)

def record(interval):
    recorded = []
    print("Start")
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    print("End")
    return recorded, startTime

def choose(words, amount):
    out = []
    if len(words) <= amount:
        return words
    elif amount == 1:
        return [words[len(words//2)]]
    tempWords = words
    while True:
        if len(out) == amount or len(tempWords) == 1:
            return out
        mid = len(tempWords)//2
        out.append(tempWords.pop(mid))

data, start = record(interval)
i = inter.Calculation(data, start, Upf)
for i in choose(i.wordsOut, 4):
    print(i.word)
print(i.toString())