import sqlite3 as sq

class DBStuff():
    
    def __init__(self, dbName):
        self.dbName = dbName
        self.conn = self.connection()
        if (self.conn != None):
            self.cursor = self.conn.cursor()
        self.setupTables()
    
    def __del__(self):
        self.conn.commit()
        self.conn.close()   
        
    def connection(self):
        conn = sq.connect(self.dbName)
        return conn
    
    def setupTables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS keyPresses (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, key TEXT, key_action TEXT, time_of_action REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sessions (SessionID INTEGER PRIMARY KEY, average_hold_time REAL, average_float_time REAL, session_length_keys INTEGER, session_length_time	REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pairs (pair_id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, key TEXT, holdtime REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS loginInfo (id INTEGER PRIMARY KEY AUTOINCREMENT, UserID TEXT, EncPassword TEXT)")
        self.conn.commit()

    def insertKeyPresses(self, data):
        session = 0
        sessionID = self.cursor.execute("SELECT MAX(session_id) FROM keyPresses").fetchone()[0]
        if (str(sessionID) != "None"):
            session = sessionID + 1
            for x in data:
                self.cursor.execute("INSERT INTO keyPresses (session_id, key, key_action, time_of_action) VALUES (?, ?, ?, ?)", (session, x[0], x[2], x[1]))
                self.conn.commit()
        else:
            for x in data:
                self.cursor.execute("INSERT INTO keyPresses (session_id, key, key_action, time_of_action) VALUES (?, ?, ?, ?)", (session, x[0], x[2], x[1]))
                self.conn.commit()
    
    def insertSessions(self, holdTimes, avgHoldTimes, floatTimes, data):
        length_keys = 0
        for y in holdTimes:
            for i in range(1, len(y)):
                length_keys +=1
        length_time = data[len(data)-1][1] - data[0][1]
        totalHold = 0
        countHold = 0
        for i in avgHoldTimes:
            totalHold += i[1]
            countHold += 1
        sessionAvgHoldTime = totalHold/countHold
        
        totalFloat = 0
        countFloat = 0
        for i in floatTimes:
            totalFloat += i[2]
            countFloat += 1
        sessionAvgFloatTime = totalFloat/countFloat
        self.cursor.execute("INSERT INTO sessions (SessionID, average_hold_time, average_float_time, session_length_keys, session_length_time) VALUES (?,?, ?, ?, ?)", (session, sessionAvgHoldTime, sessionAvgFloatTime, length_keys, length_time))
        self.conn.commit()
    
    def insertPairs(self, session, data):
        for x in data:
            for i in range(1, len(x)):
                self.cursor.execute("INSERT INTO pairs (session_id, key, holdtime) VALUES (?, ?, ?)", (session, x[0], x[i]))
            self.conn.commit()
    
    def insertLoginInfoEnc(self, uName, Pw):
        self.cursor.execute("INSERT INTO loginInfo (UserID, EncPassword) VALUES (?, ?)", (uName, Pw))
        self.conn.commit()
        
    def uNameExists(self, uName):
        retrievedUserName = self.cursor.execute("SELECT UserId FROM loginInfo where UserId = ?", (uName,)).fetchone()
        if retrievedUserName == None:
            return False
        else:
            return True
        
    def retrievePW(self, uName):
        if self.uNameExists(uName):
            retrievedPassword = self.cursor.execute("SELECT EncPassword FROM loginInfo where UserId = ?", (uName,)).fetchone()[0]
            return retrievedPassword
        else:
            return None