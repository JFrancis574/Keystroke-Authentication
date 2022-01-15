import keyboard
import time


def record(interval):
    recorded = []
    keyBoardHook = keyboard.hook(recorded.append)
    
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    return recorded


print(record(5.0))