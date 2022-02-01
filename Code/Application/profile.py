import os.path
class Profile:
    
    def __init__(self, uName, PW):
        self.user = uName
        self.pw = PW
        self.userPath = None
        self.setup()
        
    def setup(self):
        userPath = os.getcwd() + '/Data/uName/'
        if os.path.exists(userPath):
            self.userPath = userPath
        else:
            os.mkdir(userPath)
            self.userPath = userPath
        
        