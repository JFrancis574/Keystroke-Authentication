import getpass
import os.path
from KeyboardClass import Keyboard as k
from random import choice
from string import ascii_lowercase

class User_Profile:
    def __init__(self, keyName=None):
        """The User Profile class. Contains methods that store the users path along with their data.

        Args:
            keyName (string, optional): The default keyboard name. Defaults to None.
        """
        self.user = getpass.getuser()
        self.userPath = os.getcwd() + '/Data/'+self.user+'/'
        self.newUser = self.checkNew()
        self.setup()
        self.keyboards = []
        self.currentKeyboard = self.addKeyboard(None)
    
    def setup(self):
        """Creates all base directories for the user
        """
        print("Setup for user profile")
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
        
    def addKeyboard(self, name=None):
        """Used to create a new keyboard for the user

        Args:
            name (string, optional): The new keyboards name. Defaults to None.

        Returns:
            Keyboard: Returns a new keyboard object
        """
        if name == None:
            # If no name is specified, then select the first keyboard in the users directory
            if len(os.listdir(self.userPath)) != 0:
                name = os.listdir(self.userPath)[0]
            else:
                # If none exist, randomly generate a name
                letters = ascii_lowercase
                # Uses pythons inbuilt random function
                # https://docs.python.org/3/library/random.html
                name = ''.join(choice(letters) for i in range(10))
        newKeyboard = k(name, self.userPath)
        self.keyboards.append(newKeyboard)
        self.currentKeyboard = newKeyboard
        return newKeyboard
        
    def changeKeyboard(self, name):
        """Change the keyboard by name

        Args:
            name (string): The name of the new keyboard

        Returns:
            bool: If the change was successful. e.g. if the keyboard you want to change to exists. 
        """
        for x in self.keyboards:
            if x.name == name:
                self.currentKeyboard = x
                return True
        return False
    
    def setNew(self, Bool):
        """Simply sets the flag if the user is new

        Args:
            Bool (bool): What to set the flag to
        """
        self.newUser = Bool
        
    def checkNew(self):
        """Checks if the User_Profile already exists

        Returns:
            bool: True if does exist, false if not
        """
        parent = os.getcwd()
        newDirectory = '/Data/'+self.user+'/'
        return not os.path.exists(parent+newDirectory)
    
    def getKeyboardPath(self):
        """Returns theh current keyboards path

        Returns:
            string: The current keyboards path
        """
        return self.currentKeyboard.getPath()
    
        