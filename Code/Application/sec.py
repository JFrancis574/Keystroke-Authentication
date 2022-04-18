import pickle
import timeit
import Training as t
import Interval as i
import user_profile as pf
import keyboard
import time
import seaborn as sns
from matplotlib import pyplot as plt


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
# data, start = record(60)
# print(start)

file = open("data.pickle", 'rb')
data = pickle.load(file)
start = 1649857380.5629547
prof = pf.User_Profile()
presave = t.Training(data, start, prof, 1, 0)

# file = open("data.pickle", 'wb')
# pickle.dump(data, file)
# file.close()
  
interval = i.Calculation(data, start, prof, 1)
for x in range(2, interval.noWords, 2):
    print(x)
    interval.chosenAmount = x
    interval.chosen = interval.choose()
    start = timeit.default_timer()
    _, _ = interval.validation(mode='rnl')
    times[x] = timeit.default_timer() - start

sns.regplot(x=list(times.keys()), y=list(times.values()), ci=None)
plt.title("Words Chosen vs Time Taken")
plt.xlabel("Words Chosen")
plt.ylabel("Time Taken")
plt.show()








