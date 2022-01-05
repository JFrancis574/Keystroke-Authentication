import keyboard
import time
def record_until(any_key = False):
    interval = 10 # ten seconds
    recorded = []
    startTime = time.time()
    keyboard.hook(recorded.append) # need this to capture terminator

    wait, unlock = keyboard._make_wait_and_unlock()

    if any_key:
        hook = keyboard.hook(unlock)

    wait()

    try:
        keyboard.remove_hotkey(hook)
    except ValueError: pass

    return recorded


record_until(any_key=True)