import os


class Keyboard:
    def __init__(self,name, pf):
        """Keyboard class

        Args:
            name (string): The name of the keyboard
            pf (User_Profile): profile to store the keyboard under
        """
        self.name = name
        self.userPath = pf
        self.setup()
        
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.userPath+self.name
    
    def setup(self):
        if not os.path.exists(self.userPath+self.name):
            os.mkdir(self.userPath+self.name)
