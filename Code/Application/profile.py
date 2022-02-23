import getpass
import os.path
import time
from KeyboardClass import Keyboard

class Profile:
    def __init__(self, uName, PW):
        self.user = getpass.getuser()
        self.userPath = os.getcwd() + '/Data/'+self.user+'/'
        self.setup()
        self.keyboards = []
        self.currentKeyboard = None
    
    def setup(self):
        parent = os.getcwd()
        newDirectory = 'Data/'+self.user+'/'
        try:
            os.mkdir(os.path.join(parent,'Data'))
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join(parent,newDirectory))
        except FileExistsError:
            pass
        
    def addKeyboard(self, vendorDeets, name):
        pluggedTime = time.time()
        newKeyboard = Keyboard(pluggedTime, vendorDeets, name)
        self.keyboards.append(newKeyboard)
        self.currentKeyboard = newKeyboard
        
    def changeKeyboard(self, name):
        for x in self.keyboards:
            if x.name == name:
                self.currentKeyboard = x
                return True
        return False
            
        