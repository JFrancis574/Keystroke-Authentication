import getpass
import os.path
from KeyboardClass import Keyboard as k

class Profile:
    def __init__(self, keyName):
        self.user = getpass.getuser()
        self.userPath = os.getcwd() + '/Data/'+self.user+'/'
        self.newUser = self.checkNew()
        self.setup()
        self.keyboards = []
        self.currentKeyboard = self.addKeyboard(keyName)
    
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
        
    def addKeyboard(self, name):
        newKeyboard = k(name, self.userPath)
        self.keyboards.append(newKeyboard)
        return newKeyboard
        
    def changeKeyboard(self, name):
        for x in self.keyboards:
            if x.name == name:
                self.currentKeyboard = x
                return True
        return False
    
    def setNew(self, Bool):
        self.newUser = Bool
        
    def checkNew(self):
        parent = os.getcwd()
        newDirectory = '/Data/'+self.user+'/'
        return not os.path.exists(parent+newDirectory)
    
    def getKeyboardPath(self):
        return self.currentKeyboard.getPath()
    
        