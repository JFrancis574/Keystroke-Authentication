import random
import time
import keyboard
import csv

def tester(delay, words, type='v'):
    if type == 'v':
        variableRange = delay/10
    else:
        variableRange = 0
    time.sleep(2)
    datafile = open('data.csv', 'r')
    myreader = csv.reader(datafile)
    for row in myreader:
        for value in row:
            keyboard.write(value)
            if type != 'v':
                time.sleep(delay)
            else:
                print(random.uniform(delay, delay+(variableRange)*2))
                time.sleep(random.uniform(delay, delay+(variableRange)*2))
        keyboard.write(' ')
        
tester(0.1, 'tt', 'v')