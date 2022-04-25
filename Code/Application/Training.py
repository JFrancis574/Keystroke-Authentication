import json
import os
from Interval import Calculation

class Training(Calculation):
    
    def __init__(self, raw, startTime, pf, semCheck, stop, validation=0):
        """Training version of the Calculation Class

        Args:
            raw (dict): The raw input data
            startTime (timestamp): The timestamp at which the raw data was collected
            pf (User_Profile): The user profile which the data belongs to
            semCheck (int): Flag which controls if to check the semantics data
            validation (int, optional): If to perform validation as well. Defaults to 0
        """
        super().__init__(raw, startTime, pf, semCheck, lambda: stop)
        self.wordTrainingSet = 100
        self.semantics = self.usesPunc()
        self.success = self.genKDSAndSave()
    
    def genKDSAndSave(self):
        for x in range(0, len(self.wordsOut)):
            fileName = self.wordsOut[x].word+'.json'
            Kds = self.wordsOut[x].compress()
            if os.path.exists(self.pf.getKeyboardPath()+'/'+fileName):
                pass
            else:
                with open(self.pf.getKeyboardPath()+'/'+fileName, 'w') as write_file:
                    json.dump(Kds, write_file)
                write_file.close()
        with open(self.pf.getKeyboardPath()+'/Semantics.json', 'w') as write_file:
                json.dump(self.semantics, write_file)
        write_file.close()
        return True
    
    def usesPunc(self):
        out = {}
        for x in self.pairs:
            if x[0] in ['alt', 'shift', 'ctrl', 'caps lock']:
                out[x[0]] = 1
        return out