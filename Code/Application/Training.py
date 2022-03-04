import json
import os
from Interval import Calculation

class Training(Calculation):
    
    def __init__(self, raw, startTime, pf):
        super().__init__(raw, startTime, pf)
        
    
    def genKDSAndSave(self):
        for x in range(0, len(self.wordsOut)):
            fileName = self.wordsOut[x].word+'.json'
            Kds = self.wordsOut[x].compress()
            print(self.pf.userPath)
            if os.path.exists(self.pf.userPath+fileName):
                pass
            else:
                with open(self.pf.userPath+fileName, 'w') as write_file:
                    json.dump(Kds, write_file)
                write_file.close()
             