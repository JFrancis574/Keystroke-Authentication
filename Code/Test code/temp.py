# Data in format:
# [key, down, up]
import pickle as p
import time
from keyboardTest import *

keysInput = [
    [
        ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0004, 0.0006], ['l', 0.0006, 0.0007], ['o', 0.0007, 0.0008]
    ],
    [
        ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0007, 0.0009], ['p', 0.0009, 0.0009]
    ],
    [
        ['j', 0.0010, 0.0011], ['a', 0.0013, 0.0014], ['c', 0.0017, 0.0020], ['k', 0.0022, 0.0025]
    ],
    [
        ['g', 0.0027, 0.0030], ['a', 0.0035, 0.0044], ['c', 0.0050, 0.0070], ['k', 0.0072, 0.0075]
    ]
]

startTime = time.time()
pair = process(startTime, record(60.0))

outFile = open('60SecondTestDataToBeChecked.p', 'wb')
p.dump(pair, outFile)
outFile.close()
