# ctypes implementation inside python standard lib
# https://docs.python.org/3/library/ctypes.html
import ctypes

# getpass implementation inside python standard lib
# https://docs.python.org/3/library/getpass.html
import getpass

# JSON implementation inside Python Standard Lib
# https://docs.python.org/3/library/json.html
import json

# math implementation inside Python Standard Lib
# https://docs.python.org/3/library/math.html
import math

# OS implementation inside Python Standard Lib
# https://docs.python.org/3/library/os.html
import os.path

# String implementation inside Python Standard Lib
# https://docs.python.org/3/library/string.html
import string

# subprocess implementation inside Python Standard Lib
# https://docs.python.org/3/library/subprocess.html
import subprocess

# NumPy implementation by NumPy
# https://numpy.org/
# Last updated: 02/05/2022
import numpy as np

# FastDTW implementation by slaypni
# https://github.com/slaypni/fastdtw                 
from fastdtw import fastdtw

# Euclidean distance implementation by scipy
# https://scipy.org/
from scipy.spatial.distance import euclidean

import Word as w

class Calculation:
    """Calculation class that literally does everything
    """
    def __init__(self, raw, startTime, pf, semanticsCheck):
        """Preparing the class

        Args:
            raw (array): The raw data fed in, typically consists of a lot of keyboard events
            startTime (float): The starttime of the interval
            pf (Profile): The users profile
            semanticsCheck (int): Used to determine whether the semantics check is used
        """
        self.raw = raw
        self.pf = pf
        self.roundInterval = 4
        self.startTime = startTime
        self.chosenAmount = 4
        self.processed = self.process()
        self.pairs = self.rawPairs()
        self.wordsOut, self.semantics = self.words()
        self.noWords = len(self.wordsOut)
        self.chosen = self.choose()
        self.semanticsCheck = semanticsCheck
        
    def process(self):
        """
        Converts the raw keystroke data into a pair consisting of both the up and down actions.

        Returns:
            2D array: 2 dimensional array consisting of a seperate array for each key action. Converts the time into one that can actually be used.
        """
        if len(self.raw) == 0:
            return []
        rawKeys = []
        for record in self.raw:
            rawKeys.append([record.name, (record.time - self.startTime), record.event_type])
        return rawKeys
    
    def rawPairs(self):
        """
        Converts the array from the process function into key pairs

        Returns:
            2D array: Consisting of a pair of actions from the array above.
        """
        pairsArray = []
        for i in range(len(self.processed)):
            try:
                if (self.processed[i][2] == 'down' and self.processed[i+1][2] == 'up' and self.processed[i][0].lower() == self.processed[i+1][0].lower()):
                    # If the next value in the array is the up action
                    pairsArray.append([self.processed[i][0], self.processed[i][1], self.processed[i+1][1]])
                else:
                    # Otherwise, search for the next opposing action and pair them up
                    for x in range(i, len(self.processed)):
                        if (self.processed[x][0].lower() == self.processed[i][0].lower() and self.processed[x][2] == 'up' and self.processed[i][2] == 'down'):
                            pairsArray.append([self.processed[i][0], self.processed[i][1], self.processed[x][1]])
                            break        
            except IndexError:
                pass
        return pairsArray
    
    def words(self):
        """Converts the raw pairs into "words" using rules. A word is defined as all pairs that occur up until either a punctuation pair (e.g. space, !, etc)

        Returns:
            list: A list of word objects
        """
        bannedPunc = ['space', 'enter','play/pause media','alttab', 'eqdown', 'right', 'left', 'up', 'down', 'tab','alt', 'shift', 'ctrl']
        currentWord = []
        output = []
        semantics = {} # This is used to store details on whether the user uses caps lock or shift. Essentially another security method
        for j, i in enumerate(self.pairs):
            if i[0] in ['shift', 'caps lock']:
                semantics[i[0]] = 1
            elif i[0] not in bannedPunc and i[0] not in string.punctuation:
                # If there is a backspace pair, remove the last character pair
                if i[0] == 'backspace':
                    if len(currentWord) != 0:
                        currentWord.pop(-1)
                        if i == self.pairs[-1]:
                            output.append(w.Word(currentWord))
                            currentWord = []
                    else:
                        if len(output) != 0:
                            # If there is no word currently being stored, remove the last one and remove the last character pair.
                            currentWord = output.pop(-1).raw
                elif i == self.pairs[-1]:
                    # If i is the last pair
                    currentWord.append(i)
                    if len(currentWord) != 0:
                        output.append(w.Word(currentWord))
                    currentWord = []
                else:
                    currentWord.append(i)
            else:
                # Punctuation handling, this deals with words such as didn't and user-generated
                if i[0] in ['space', '.', 'enter', ',',':',';']:
                    if len(currentWord) != 0:
                        output.append(w.Word(currentWord))
                    currentWord = []
                elif i[0] == "'" or i[0] == '-':
                    if len(currentWord) == 0:
                        pass
                    else:
                        try:
                            if currentWord[-1][0].isalpha() and self.pairs[j+1][0].isalpha():
                                currentWord.append(i)
                            else:
                                output.append(w.Word(currentWord))
                                currentWord = []
                        except IndexError:
                            output.append(w.Word(currentWord))
                            currentWord = []
                else:
                    pass
        return output, semantics
        
    def choose(self):
        """Chooses x amount of words from all the words the user types in the interval. The x is set by the self.chosenAmount attribute. O(n)

        Returns:
            list: list of word objects
        """
        
        out = []
        # Base cases
        if len(self.wordsOut) <= self.chosenAmount:
            return self.wordsOut
        elif self.chosenAmount == 1:
            # Just selects the middle word
            return [self.wordsOut[len(self.wordsOut//2)]]
        
        tempWords = self.wordsOut.copy()
        while True:
            if len(out) == self.chosenAmount or len(tempWords) == 1:
                return out
            mid = len(tempWords)//2
            out.append(tempWords.pop(mid))
    
    def validation(self, mode='r'):
        """The big boi. This essentially decided whether to accept the user or to kick the user out. Also handles the security aspect.

        Args:
            mode (str, optional): This chooses whether this function is in test mode or not. Defaults to 'r'. r = real, t = test, rnl = real no lock

        Returns:
            Bool: If the user has been validated or not
            list: All the words chosen that have failed
        """
        distances = {}
        if mode in ['r', 'rnl', 't']:
            # For every word that has been chosen.
            for x in range(0, len(self.chosen)):
                fileName = self.chosen[x].word+'.json'
                if os.path.exists(self.pf.getKeyboardPath()+'/'+fileName):
                    # Loading in the data from the word files
                    with open(self.pf.getKeyboardPath()+'/'+fileName, 'r') as read_file:
                        dataIn = self.decompress(json.load(read_file))
                    read_file.close()
                    
                    # Beautifying and forming the correct data
                    inInterval = np.array(list(self.chosen[x].KDSWord().values()))
                    fromFile = np.array(list(dataIn.values()))


                    # FastDTW implementation by slaypni
                    # https://github.com/slaypni/fastdtw
                    
                    # Euclidean distance implementation by scipy
                    # https://scipy.org/
                    euclideanDistance, path = fastdtw(fromFile, inInterval, dist=euclidean)
                    
                    ff_path, ii_path = zip(*path)
                    ff_path = np.asarray(ff_path)
                    ii_path = np.asarray(ii_path)
                    ff_warped = fromFile[ff_path]
                    ii_warped = inInterval[ii_path]

                    # Correlation Coefficant
                    cov = 0
                    XSum = 0
                    YSum = 0
                    Xmean = sum(ff_warped)/len(ff_warped)
                    Ymean = sum(ii_warped)/len(ii_warped)
                    
                    for i in range(len(ff_warped)):
                        cov += (ff_warped[i] - Xmean)*(ii_warped[i] - Ymean)
                        XSum += math.pow(ff_warped[i]-Xmean, 2)
                        YSum += math.pow(ii_warped[i]-Ymean, 2)
                    
                
                    correlationCoEfficant = cov/((math.sqrt(XSum)*(math.sqrt(YSum))))
                    distances[x] = [euclideanDistance, correlationCoEfficant]
                else:
                    # If the word has never been seen before
                    distances[x] = [None, None]
            
            
                
            bandingEuc = 1000 # The range at which the euc distance is the same user.
            bandingCorr = 0.80 # The range at which the Correlation distance is the same user.
            bandingChange = 0.02 # The decrease for correct semantics.
            
            
            # Semantics stuff, currently a semantics match in terms of shift and caps lock will lead to the correlation banding being shorter
            if self.semanticsCheck != 0 or len(self.semantics) == 0:
                loadIn = self.validationSemantics()
                if loadIn != -1 and len(self.semantics) != 0:
                    if 'shift' in loadIn and 'shift' in self.semantics and 'caps lock' not in self.semantics and 'caps lock' not in loadIn:
                        bandingCorr = bandingCorr - bandingChange
                    elif 'shift' not in loadIn and 'shift' not in self.semantics and 'caps lock' in self.semantics and 'caps lock' in loadIn:
                        bandingCorr = bandingCorr - bandingChange
                    elif ('shift' in loadIn and 'shift' not in self.semantics and 'caps lock' in self.semantics and 'caps lock' not in loadIn) or ('shift' not in loadIn and 'shift' in self.semantics and 'caps lock' in self.semantics and 'caps lock' not in loadIn):
                        if bandingCorr + bandingChange > 0.99:
                            pass
                        else:
                            bandingCorr = bandingCorr + bandingChange
                    else:
                        pass
            
            wordCheck = []
            for j in list(distances.values()):
                if j[0] == None:
                    wordCheck.append(None)
                # Both are inside the banding = same user
                elif j[0] <= bandingEuc and j[1] >= bandingCorr:
                    wordCheck.append(True)
                # Correlation is far more important
                elif j[1] >= bandingCorr and j[0] > bandingEuc:
                    wordCheck.append(True)
                else:
                    wordCheck.append(False)

            # For use in testing only
            if mode == 't':
                return distances, wordCheck
            

            # Decision maker
            if len(wordCheck) != 1:
                if False not in wordCheck and None not in wordCheck:
                    return True, []
                elif True in wordCheck and None in wordCheck and False not in wordCheck:
                    self.update([i for i, j  in enumerate(wordCheck) if j == None])
                    return True, []
                elif False in wordCheck and None in wordCheck and True not in wordCheck:
                    # Code to lock pc
                    if mode != 'rnl':
                        self.lockPc()
                        # The user then re-authenticates
                        # Check if user re-authenticates successfully
                        while True:
                            if self.checkLocked():
                                break
                        # If the same user,
                        if getpass.getuser() == self.pf.user:
                            # Update the relevant words and the semantics stored
                            self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                            self.updateSemantics()
                            return True, []
                        else:
                            # Otherwise, set up a new profile
                            return 'New', []
                    else:
                        return True, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
                    
                elif True not in wordCheck and False not in wordCheck and None in wordCheck:
                    if mode != 'rnl':
                        self.lockPc()
                        # The user then re-authenticates
                        # Check if user re-authenticates successfully
                        while True:
                            if self.checkLocked():
                                break
                        # If the same user,
                        if getpass.getuser() == self.pf.user:
                            # Update the relevant words and the semantics stored
                            self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                            self.updateSemantics()
                            return True, []
                        else:
                            # Otherwise, set up a new profile
                            return 'New', []
                    else:
                        return True, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
                
                elif True in wordCheck and False in wordCheck and None not in wordCheck:
                        if mode != 'rnl':
                            self.lockPc()
                            # The user then re-authenticates
                            # Check if user re-authenticates successfully
                            while True:
                                if self.checkLocked():
                                    break
                            # If the same user,
                            if getpass.getuser() == self.pf.user:
                                # Update the relevant words and the semantics stored
                                self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                                self.updateSemantics()
                                return True, []
                            else:
                                # Otherwise, set up a new profile
                                return 'New', []
                        else:
                            return True, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
                        
                elif True in wordCheck and False in wordCheck and None in wordCheck:
                    if mode != 'rnl':
                        self.lockPc()
                        # The user then re-authenticates
                        # Check if user re-authenticates successfully
                        while True:
                            if self.checkLocked():
                                break
                        # If the same user,
                        if getpass.getuser() == self.pf.user:
                            # Update the relevant words and the semantics stored
                            self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                            self.updateSemantics()
                            return True, []
                        else:
                            # Otherwise, set up a new profile
                            return 'New', []
                    else:
                        return True, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
               
                else:
                    if mode != 'rnl':
                        self.lockPc()
                        # The user then re-authenticates
                        # Check if user re-authenticates successfully
                        while True:
                            if self.checkLocked():
                                break
                        # If the same user,
                        if getpass.getuser() == self.pf.user:
                            # Update the relevant words and the semantics stored
                            self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                            self.updateSemantics()
                            return True, []
                        else:
                            # Otherwise, set up a new profile
                            return 'New', []
                    else:
                        return True, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
                
            else:
                if True in wordCheck:
                    return True, []
                elif False in wordCheck:
                    if mode != 'rnl':
                        self.lockPc()
                        while True:
                            if self.checkLocked():
                                break
                        # If the same user,
                        if getpass.getuser() == self.pf.user:
                            # Update the relevant words and the semantics stored
                            self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                            self.updateSemantics()
                            return True, []
                        else:
                            # Otherwise, set up a new profile
                            return 'New', []
                    else:
                        return False, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
                    
                elif None in wordCheck:
                    if mode != 'rnl':
                        self.lockPc()
                        while True:
                            if self.checkLocked():
                                break
                        # If the same user,
                        if getpass.getuser() == self.pf.user:
                            # Update the relevant words and the semantics stored
                            self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                            self.updateSemantics()
                            return True, []
                        else:
                            # Otherwise, set up a new profile
                            return 'New', []
                    else:
                        self.update([i for i, j  in enumerate(wordCheck) if j == None or j == False])
                        self.updateSemantics()
                        return False, [i for i, j  in enumerate(wordCheck) if j == None or j == False]
        else:
            # Only in use in test mode
            # Current reg system, just generate and save KDS for every word
            for x in range(0, len(self.wordsOut)):
                fileName = self.wordsOut[x].word+'.json'
                Kds = self.wordsOut[x].compress()
                # Kds = self.wordsOut[x].KDSWord()
                if os.path.exists(self.pf.getKeyboardPath()+'/'+fileName):
                    pass
                else:
                    with open(self.pf.getKeyboardPath()+'/'+fileName, 'w') as write_file:
                        json.dump(Kds, write_file)
                    write_file.close()
            return "Bench Created", []
        
    def decompress(self, data):
        """Used to decompress the data that is stored in and convert it into the required dictionary

        Args:
            data (dictionary): The compressed data

        Returns:
            dict: The uncompressed data, very large
        """
        outDict = {}
        for x in data:
            start = float(list(x.values())[0][0])
            end = float(list(x.values())[0][1])
            value = float(list(x.values())[1])

            start10x = int(start*10000)
            end10x = int(round(end*10000,0))+1
            for x in range(start10x, end10x):
                if start != end:
                    outDict[x/10000] = value
                else:
                    outDict[start] = value
                    outDict[end] = value
        return outDict
    
    def __str__(self):
        """Simple display of all words and all chosen words

        Returns:
            string: Nicely formatted string
        """
        out = "Words: "
        for x in self.wordsOut:
            out += "\n"+x.toString()
        out += "\nChosen: "
        for i in self.chosen:
            out += "\n"+i.toString()
        return out
    
    def update(self, indexes):
        """Used to update word files with new data. Used typically after the user has re-authenticated

        Args:
            indexes (array): The indexes of the words that need updating in the chosen list
        """
        if len(indexes) == len(self.chosen):
            intruderWords = self.chosen
        else:
            intruderWords = [self.chosen[indexes[i]] for i in range(len(indexes))]
        for x in intruderWords:
            fileName = x.word+'.json'
            Kds = x.compress()
            with open(self.pf.getKeyboardPath()+'/'+fileName, 'w') as write_file:
                json.dump(Kds, write_file)
            write_file.close()
            
    def lockPc(self):
        """Used to lock the pc
        """
        cmd='rundll32.exe user32.dll, LockWorkStation'
        subprocess.call(cmd)
            
    def checkLocked(self):
        """Check if the pc is locked using ctypes. PAINFUL

        Returns:
            bool: False if locked, true otherwise
        """
        user32 = ctypes.windll.User32
        if (user32.GetForegroundWindow() % 10 != 0):
            return False
        else:
            return True
        
    def validationSemantics(self):
        """Grabs the semantics data.

        Returns:
            int or dictionary: -1 if no semantics data exists, or the data if it does.
        """
        if len(self.semantics) == 0:
            return -1
        if os.path.exists(self.pf.getKeyboardPath()+'/Semantics.json'):
            with open(self.pf.getKeyboardPath()+'/Semantics.json', 'r') as read_file:
                dataIn = json.load(read_file)
            read_file.close()
            return dataIn
        else:
            return -1
        
    def updateSemantics(self):
        """Used to update the semantics
        """
        if len(self.semantics) == 0:
            return
        with open(self.pf.getKeyboardPath()+'/Semantics.json', 'w') as write_file:
            json.dump(self.semantics, write_file)
        write_file.close()
