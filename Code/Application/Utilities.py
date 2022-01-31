import os.path
import DBConnection as db

class Utilities:
    def __init__(self, uName):
        self.uName = uName

    def testUserData(self):
        try:
            os.mkdir(os.getcwd()+'/Data/WordData')
            return True
        except FileExistsError:
            return False

    def UserData(self):
        try:
            os.mkdir(os.getcwd()+'/UserData/'+self.uName)
            return True
        except FileExistsError:
            return False
        
    def setupDone(self):
        if os.path.exists(os.getcwd()+'/UserData/'+self.uName):
            return True
        else:
            return False
        
    def getUserDataPath(self):
        if self.setupDone():
            return os.getcwd()+'/UserData/'+self.uName
        else:
            self.UserData()
            return os.getcwd()+'/UserData/'+self.uName+'/'
        
    def getUserTestDataPath(self):
        return os.getcwd()+'/Data/WordData/'