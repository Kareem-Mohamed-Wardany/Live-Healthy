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

    def Select(self, Query, Values=None):
        if Values is None:
            Values = []
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)
        return mycursor.fetchall()

    def Insert(self, Query, Values=None):
        if Values is None:
            Values = []
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)

    def Commit(self):
        self.mydb.commit()

    # Check link for more info https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, "rb") as file:
            binaryData = file.read()
        return binaryData

    def write_file(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, "wb") as file:
            file.write(data)
