import timeit
import Training as t
import Interval as i
import user_profile as pf
import keyboard
import time
import seaborn as sns
import matplotlib as plt


def record(interval):
    recorded = []
    startTime = time.time()
    keyBoardHook = keyboard.hook(recorded.append)
    print("RECORDING")
    time.sleep(interval)
    keyboard.unhook(keyBoardHook)
    print("NOT")
    return recorded, startTime

times = {}
data, start = record(60)
prof = pf.User_Profile()
presave = t.Training(data, start, prof, 1, 0)

# 4 words chosen
interval = i.Calculation(data, start, prof, 1)
start = timeit.default_timer()
_, _ = interval.validation(mode='rnl')
times[4] = timeit.default_timer() - start

# 6 words chosen
interval = i.Calculation(data, start, prof, 1)
interval.chosenAmount = 6
interval.chosen = interval.choose()
print(len(interval.chosen))
start = timeit.default_timer()
_, _ = interval.validation(mode='rnl')
times[6] = timeit.default_timer() - start

# 8 words chosen
interval = i.Calculation(data, start, prof, 1)
interval.chosenAmount = 8
interval.chosen = interval.choose()
print(len(interval.chosen))
start = timeit.default_timer()
_, _ = interval.validation(mode='rnl')
times[8] = timeit.default_timer() - start

# 10 words chosen

interval = i.Calculation(data, start, prof, 1)
interval.chosenAmount = 10
interval.chosen = interval.choose()
print(len(interval.chosen))
start = timeit.default_timer()
_, _ = interval.validation(mode='rnl')
times[10] = timeit.default_timer() - start

# 12 words chosen

interval = i.Calculation(data, start, prof, 1)
interval.chosenAmount = 12
interval.chosen = interval.choose()
print(len(interval.chosen))
start = timeit.default_timer()
_, _ = interval.validation(mode='rnl')
times[12] = timeit.default_timer() - start

print(times)

sns.regplot(x=times.keys, y=float(times.values()), ci=None)
plt.title("Words Chosen vs Time Taken")
plt.xlabel("Words Chosen")
plt.ylabel("Time Taken")
plt.show()








