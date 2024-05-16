from django.db import models

class Driver(models.Model):
    driverID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="", unique=True)
    phone = models.CharField(max_length=12, default="", unique=True)
    password = models.CharField(max_length=50, default="")
    vehicle_number = models.CharField(max_length=15, default="")
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    vehicle_type = models.CharField(max_length=20, default="")
    rating = models.FloatField(default=5)
    available = models.BooleanField(default=False)

    def __str__(self):
        return str(self.driverID)

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="", unique=True)
    phone = models.CharField(max_length=12, default="", unique=True)
    password = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.userID)

class Ride(models.Model):
    rideID = models.AutoField(primary_key=True)
    userID = models.IntegerField(default=1)
    driverID = models.IntegerField(default=1)
    start_lat = models.FloatField(default=0)
    end_lat = models.FloatField(default=0)
    start_long = models.FloatField(default=0)
    end_long = models.FloatField(default=0)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    advanced_booking = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.rideID)
