import json
import os.path
import pickle

from keyboardTestMac import KDSWordByWord, rawPairs, words

try:
    os.mkdir(os.getcwd()+'/Data/WordData')
except FileExistsError:
    pass

infile = open(os.getcwd()+"/Data/Pickles/60SecondTestData",'rb')  
intervalData = pickle.load(infile)
infile.close()

infile = open(os.getcwd()+"/Data/Pickles/Hello1",'rb')
singleWord = pickle.load(infile)
infile.close()

intervalOut = KDSWordByWord(words(rawPairs(intervalData)),4)
singleWordOut = KDSWordByWord(words(rawPairs(singleWord)),4)

for i in range(0, len(intervalOut)):
    word = ""
    for x in words(rawPairs(intervalData))[i]:
        word+= x[0]
    fileName = word +'.json'
    if os.path.exists(os.getcwd()+"/Data/WordData/"+fileName):
        pass
    else:
        with open(os.getcwd()+"/Data/WordData/"+fileName, 'w') as write_file:
            json.dump(intervalOut[i][1], write_file)
        write_file.close()
