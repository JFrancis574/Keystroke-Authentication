import json
import os
from Interval import Calculation

class Training(Calculation):
    
    def __init__(self, raw, startTime, pf, semCheck, validation=0):
        super().__init__(raw, startTime, pf, semCheck)
        self.wordTrainingSet = 100
        if validation == 0:
            self.semantics = self.usesPunc()
            self.success = self.genKDSAndSave()
        else:
            pass
    
    def genKDSAndSave(self):
        if len(self.wordsOut) < self.wordTrainingSet:
            return False
        for x in range(0, len(self.wordsOut)):
            fileName = self.wordsOut[x].word+'.json'
            Kds = self.wordsOut[x].compress()
            if os.path.exists(self.pf.getKeyboardPath()+fileName):
                pass
            else:
                with open(self.pf.getKeyboardPath()+fileName, 'w') as write_file:
                    json.dump(Kds, write_file)
                write_file.close()
        with open(self.pf.getKeyboardPath()+'Semantics.json', 'w') as write_file:
                json.dump(self.semantics, write_file)
        write_file.close()
    
    def usesPunc(self):
        out = {}
        for x in self.pairs:
            if x[0] in ['alt', 'shift', 'ctrl', 'caps lock']:
                out[x[0]] = 1
        return out