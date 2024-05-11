import mysql.connector as mySql

class DriverDatabase:
    def __init__(self, dbname, tbname):
        self.dbname= dbname
        self.tbname = tbname
        self.db= mySql.connect(host = "localhost", user = "root", password = "Subash@2005", database = dbname)
        if self.db.is_connected():
            self.cursor= self.db.cursor()
        else:
            print("db not connected")
    def addDriver(self, driverID, lat, lon):
        self.cursor.execute(f"insert into {self.tbname} (driverID, latitude, longitude, distance) values ('{driverID}', '{lat}', '{lon}', 0)")
        self.db.commit()
        print("driver added")
    def calculateDistance(self, userLatitude, userLongitude):
        self.cursor.execute(f"UPDATE {self.tbname} SET distance = sqrt(pow({userLatitude}-latitude, 2) + pow({userLongitude}-longitude, 2))")
        self.db.commit()
        self.cursor.execute(f"select * from {self.tbname} order by distance limit 5")
        result = self.cursor.fetchall()
        for row in result:
            print(row)

database = DriverDatabase("drivercoords", "coordinates")
# database.addDriver(4, 13.27, 80.25)
# database.calculateDistance(13.116253, 80.224059)

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