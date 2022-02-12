import os.path

class Profile:
    def __init__(self, uName, PW):
        self.user = uName
        self.pw = PW
        self.userPath = os.getcwd() + '/Data/'+self.user+'/'
        self.setup()
    
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