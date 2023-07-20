import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Cable360224",
    )
my_cursor = mydb.cursor()

#my_cursor.execute("DROP DATABASE IF EXISTS users") #每次執行會刪除舊的

#my_cursor.execute("CREATE DATABASE users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)