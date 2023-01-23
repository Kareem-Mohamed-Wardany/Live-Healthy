import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)
print(mydb)

# Insert Query

# mycursor = mydb.cursor()
# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "record inserted.")



# Select Query

# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM customers")
# myresult = mycursor.fetchall()
# for x in myresult:
#   print(x)


# Select Query with where

# mycursor = mydb.cursor()
# sql = "SELECT * FROM customers WHERE address ='Park Lane 38'"
# mycursor.execute(sql)
# myresult = mycursor.fetchall()
# for x in myresult:
#   print(x) 

# Update Query 

# mycursor = mydb.cursor()
# sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
# mycursor.execute(sql)
# mydb.commit()
# print(mycursor.rowcount, "record(s) affected")

# Update with condition

# mycursor = mydb.cursor()
# sql = "UPDATE customers SET address = %s WHERE address = %s"
# val = ("Valley 345", "Canyon 123")
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "record(s) affected")