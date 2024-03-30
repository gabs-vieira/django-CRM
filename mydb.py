import mysql.connector


dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    auth_plugin='mysql_native_password'
)

#prepare a cursor object
cursorObject = dataBase.cursor()

#create a databse
cursorObject.execute("CREATE DATABASE elderco")

print("All Done!")