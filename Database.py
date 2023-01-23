import mysql.connector


class Database:
    # Database connection String
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Systemdb"
    )
    def Update(self, Query, Values):
        mycursor = self.mydb.cursor()
        mycursor.execute(Query, Values)

    def Select(self, Query, Values = []):
        mycursor = self.mydb.cursor()
        mycursor.execute(Query,Values)
        myresult = mycursor.fetchall()
        return myresult

    def Insert(self, Query, Values = []):
        mycursor = self.mydb.cursor()
        mycursor.execute(Query,Values)
        
    def Commit(self):
        self.mydb.commit()
