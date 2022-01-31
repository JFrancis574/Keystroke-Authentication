# Data in format:
# [key, down, up]
import json
import pickle as p
import time
from keyboardTest import *
import os.path

keysInput = [
    [
        ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0004, 0.0006], ['l', 0.0006, 0.0007], ['o', 0.0007, 0.0008]
    ]
    # ,
    # [
    #     ['h', 0.0001, 0.0002], ['e', 0.0003, 0.0004], ['l', 0.0007, 0.0009], ['p', 0.0009, 0.0009]
    # ],
    # [
    #     ['j', 0.0010, 0.0011], ['a', 0.0013, 0.0014], ['c', 0.0017, 0.0020], ['k', 0.0022, 0.0025]
    # ],
    # [
    #     ['g', 0.0027, 0.0030], ['a', 0.0035, 0.0044], ['c', 0.0050, 0.0070], ['k', 0.0072, 0.0075]
    # ]
]

KDSignal = KDSWordByWord(keysInput, 4)
print(KDSignal)

# startTime = time.time()
# print("Start")
# raw = record(60.0)
# print("Stop")
# processed = process(startTime, raw)
# fileName = 1
# while True:
#     if os.path.exists(os.getcwd()+'/Data/Pickles/'+str(fileName)):
#         fileName += 1
#     else:
#         with open(os.getcwd()+'/Data/Pickles/'+str(fileName), 'wb') as write_pickle:
#             p.dump(processed, write_pickle)
#         write_pickle.close()
#         break
# pairs = rawPairs(processed)
# wordsOut = words(pairs)
# KDSignal = KDSWordByWord(wordsOut, 2)
# count = 0
# for i in range(0, len(KDSignal)):
#     word = ""
#     for x in words(pairs)[i]:
#         word+= x[0]
#     fileName = word +'.json'
#     if os.path.exists(os.getcwd()+"/Data/WordData/"+fileName):
#         pass
#     else:
#         with open(os.getcwd()+"/Data/WordData/"+fileName, 'w') as write_file:
#             json.dump(KDSignal[i][1], write_file)
#         count += 1
#         write_file.close()

# print(len(wordsOut), count)