import json
import os
from Interval import Calculation

class Training(Calculation):
    
    def __init__(self, raw, startTime, pf):
        super().__init__(raw, startTime, pf)
        self.semantics = self.usesPunc()
        self.genKDSAndSave()
    
    def genKDSAndSave(self):
        for x in range(0, len(self.wordsOut)):
            fileName = self.wordsOut[x].word+'.json'
            Kds = self.wordsOut[x].compress()
            if os.path.exists(self.pf.userPath+fileName):
                pass
            else:
                with open(self.pf.userPath+fileName, 'w') as write_file:
                    json.dump(Kds, write_file)
                write_file.close()
        with open(self.pf.userPath+'Semantics.json', 'w') as write_file:
                json.dump(self.semantics, write_file)
        write_file.close()
    
    def usesPunc(self):
        out = {}
        for x in self.pairs:
            if x[0] in ['alt', 'shift', 'ctrl', 'caps lock']:
                out[x[0]] = 1
        return out