from getpass import getpass, getuser

import bcrypt

from DBConnection import DBStuff as db

# Get Details
username = getuser()
password = getpass()

# Encrypt
salt = bcrypt.gensalt()
encodedPW = bcrypt.hashpw(password.encode(), salt)
print(encodedPW)

# Store
DataStore = db("keyStorage.db")
DataStore.insertLoginInfoEnc(username, encodedPW)

# Check
passwordCheck = getpass()
retrievedPassword = DataStore.retrievePW(getuser())
if retrievedPassword != None and bcrypt.checkpw(passwordCheck.encode(), retrievedPassword) and DataStore.uNameExists(getuser()):
    print("Success")
