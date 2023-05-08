import mysql.connector
from Config import *


class Database:
    # Database connection String
    configfile = SystemConfig()

    __instance = None
    
    @staticmethod
    def getInstance():
        if Database.__instance is None:
            Database()
        return Database.__instance
    
    def __init__(self):
        if Database.__instance is None:
            Database.__instance = self
            self.Connect()

    def Connect(self):
        try:
            print("Connecting to")
            self.mydb = mysql.connector.connect(
                host=self.configfile.get("host"),
                user=self.configfile.get("user"),
                password=self.configfile.get("password"),
                database=self.configfile.get("database"),
            )
            self.mycursor = self.mydb.cursor()
            print("Connected")
        except Exception:
            print("Error, Database is not connected")

    def Update(self, Query, Values):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        self.mycursor.close()
        

    def Select(self, Query, Values=None):
        if Values is None:
            Values = []
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        data = self.mycursor.fetchall()
        self.mycursor.close()
        return data

    def Insert(self, Query, Values=None):
        if Values is None:
            Values = []
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        self.mycursor.close()

    def Delete(self, Query, Values=None):
        if Values is None:
            Values = []
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        self.mycursor.close()

    def Commit(self):
        self.mydb.commit()

    def Close(self):
        self.mydb.close()


def UpdateQuery(Query, Values):
    db = Database.getInstance()
    db.Update(Query, Values)
    db.Commit()

def SelectQuery(Query, Values=None):
    db = Database.getInstance()
    print("test query")
    res = db.Select(Query, Values)
    return res

def InsertQuery(Query, Values=None):
    db = Database.getInstance()
    db.Insert(Query, Values)
    db.Commit()

def DeleteQuery(Query, Values=None):
    db = Database.getInstance()
    db.Delete(Query, Values)
    db.Commit()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
        with open(filename, "wb") as file:
            file.write(data)
        file.close()