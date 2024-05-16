from rest_framework import serializers
from .models import Driver, User, Ride

class driverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['driverID', 'name', 'email', 'phone', 'password', 'vehicle_number', 'latitude', 'longitude', 'vehicle_type', 'rating', 'available']

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'name', 'email', 'phone', 'password']

class rideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['rideID', 'userID', 'driverID', 'start_lat', 'end_lat', 'start_long', 'end_long', 'time', 'date', 'advanced_booking', 'price']