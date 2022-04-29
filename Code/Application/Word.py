import numpy as np

class Word:
    """Used to store formed words
    """
    
    def __init__(self, wordData = None):
        """Used to store word objects

        Args:
            wordData (2D array, optional): the raw word data. Defaults to None.
        """

        self.raw = wordData
        self.roundValue = 4
        if wordData != None:
            self.word = self.getWordString()
            self.start = self.raw[0][1]
            self.end = self.raw[-1][2]
        else:
            self.word = None
            self.start = None
            self.end = None
        
    def getWordString(self):
        """Used to get the word in a string

        Returns:
            string: The word that is represented by this object
        """
        rawWord = ""
        for x in self.raw:
            rawWord += x[0]
        return rawWord
    
    def KDSWord(self):
        """Generate the KDS (Key down signal) for the word

        Returns:
            dict: Keys consist of timestamps with values being either 0, 0.5, 1, 1.5, 2, 2.5
        """
        KDSOutput = {}
        multiplier = int(str(1) + self.roundValue*str(0))
        if len(self.raw) != 0:
            for x in range(int(self.raw[0][1]*multiplier), int(self.raw[len(self.raw)-1][2]*multiplier)+1):
                KDSOutput[x/multiplier] = float(self.KDS(x/multiplier))
        return KDSOutput
    
    def heaviside(self, x1, x2):
        """Simple heaviside step function. Used in the KDS calculation

        Args:
            x1 (float): The timestamp that the data is currently being generated for
            x2 (float): The timestamp of the key action

        Returns:
            integer: Either 1, 0.5 or 0
        """
        if (x1 > x2):
            return 1
        elif (x1 == x2):
            return 0.5
        else:
            return 0
    
    def KDS(self, time):
        """Generates the KD function for a particular time

        Args:
            time (float): The time being tested

        Returns:
            integer: The total for all the data at that timestamp
        """
        sum = 0
        for i in range(0, len(self.raw)):
            sum += self.heaviside(time, round(self.raw[i][1], self.roundValue)) - self.heaviside(time, round(self.raw[i][2], self.roundValue))
        return sum
    
    def remap_keys(self, mapping):
        """Utility function used in the compression function in order to save the ranges as keys in the JSON

        Args:
            mapping (dictionay): The data that needs to be cleaned and formatted

        Returns:
            array: Consists of a string of key values pairs from the dictionary
        """
        return [{'range':k, 'value': v} for k, v in mapping.items()]
    
    def compress(self):
        """Compressed the KD data into ranges to save space. e.g. will convert {0.5 : 1, 0.6 : 1, 0.7 : 1, 0.8 : 0, 0.9 : 0 } into {0.5 - 0.7 : 1, 0.8 - 0.9 : 0}

        Returns:
            Dictionary: The compressed dictionary
        """
        allData = self.KDSWord()
        data = np.array(list(allData.values()))
        keys = np.array(list(allData.keys()))
        startValue = data[0]
        start = keys[0]
        endDict = {}
        for i, j in enumerate(data):
            if i == len(data)-1:
                grouping = (start, keys[i])
                endDict[grouping] = startValue
                if data[i] != startValue:
                    grouping = (keys[i], keys[i])
                    endDict[grouping] = data[i]
            elif j == startValue:
                grouping = (start, keys[i])
            else:
                endDict[grouping] = startValue
                startValue = data[i]
                start = keys[i]
                grouping = (start, keys[i])
                
        return self.remap_keys(endDict)
    
    def toString(self):
        """Simple toString()

        Returns:
            string: Descriptive text used for debugging
        """
        return self.word + ' ' + str(self.start) + ' ' + str(self.end)