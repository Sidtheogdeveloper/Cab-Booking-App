import mysql.connector as mySql

database = mySql.connect(
    host = "localhost",
    username = "root",
    password = "Subash@2005",
    database = "db"
)

cursor = database.cursor()
cursor.execute("drop table users")
database.commit()