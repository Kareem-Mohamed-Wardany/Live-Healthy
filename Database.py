import mysql.connector
from Config import *


class Database:
    # Database connection String
    config = SystemConfig()

    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.config.get("host"),
                user=self.config.get("user"),
                password=self.config.get("password"),
                database=self.config.get("database"),
            )
        except Exception:
            print("Error, Database is not connected")

    def Update(self, Query, Values):
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)
        mycursor.close()
        

    def Select(self, Query, Values=None):
        if Values is None:
            Values = []
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)
        data = mycursor.fetchall()
        mycursor.close()
        return data

    def Insert(self, Query, Values=None):
        if Values is None:
            Values = []
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)
        mycursor.close()

    def Delete(self, Query, Values=None):
        if Values is None:
            Values = []
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)
        mycursor.close()

    def Commit(self):
        self.mydb.commit()

    def Close(self):
        self.mydb.close()


def UpdateQuery(Query, Values):
    db = Database()
    db.Update(Query, Values)
    db.Commit()
    db.Close()

def SelectQuery(Query, Values=None):
    db = Database()
    res = db.Select(Query, Values)
    db.Close()
    return res

def InsertQuery(Query, Values=None):
    db = Database()
    db.Insert(Query, Values)
    db.Commit()
    db.Close()

def DeleteQuery(Query, Values=None):
    db = Database()
    db.Delete(Query, Values)
    db.Commit()
    db.Close()

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