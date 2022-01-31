import os.path
import DBConnection as db

def testUserData():
    try:
        os.mkdir(os.getcwd()+'/Data/WordData')
        return True
    except FileExistsError:
        return False

def UserData(username):
    try:
        os.mkdir(os.getcwd()+'/UserData/'+username)
        return True
    except FileExistsError:
        return False
    
def setupDone(username):
    if os.path.exists(os.getcwd()+'/UserData/'+username):
        return True
    else:
        return False
    
def getUserDataPath(username):
    if setupDone(username):
        return os.getcwd()+'/UserData/'+username
    else:
        UserData(username)
        return os.getcwd()+'/UserData/'+username+'/'
    
def getUserTestDataPath():
    return os.getcwd()+'/Data/WordData/'
        
def DBCreation():
    return db.DBStuff("keyStorage.db")