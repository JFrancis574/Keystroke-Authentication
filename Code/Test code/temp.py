import time
import keyboard

def recordUntil():
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    data = input()
    keyboard.unhook(keyBoardHook)
    return recorded, startTime

print(recordUntil())