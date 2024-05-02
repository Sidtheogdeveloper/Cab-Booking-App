import mysql.connector as mySql

class Database:
    def __init__(self, dbname):
        self.dbname= dbname
        self.db= mySql.connect(host = "localhost", user = "root", password = "Subash@2005")
        if self.db.is_connected():
            self.cursor= self.db.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
            print("DB created")
            self.cursor.execute(f"USE {dbname}")
            print("db connected")
        else:
            print("db not connected")
    def __create_table__(self, tbname):
        if self.dbname.lower()=="user":
            self.cursor.execute(f"create table {tbname} (username varchar(30), email varchar(30))")
            print("user table created")
        elif self.dbname.lower()=="driver":
            self.cursor.execute(f"create table {tbname} (username varchar(30), email varchar(30))")
            print("driver table created")
        self.db.commit()

user= Database(dbname="USER")
name= input("enter your name: ")
user.__create_table__(tbname= name)

'''
database = mySql.connect(
    host = "localhost",
    username = "root",
    password = "Subash@2005",
    database = "db"
)

cursor = database.cursor()
cursor.execute("drop table users")
database.commit()
'''