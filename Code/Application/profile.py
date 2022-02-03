import os.path

class Profile:
    def __init__(self, uName, PW):
        self.user = uName
        self.pw = PW
        self.userPath = os.getcwd() + '/Data/'+self.user+'/'
        