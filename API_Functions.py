import requests, requests.exceptions
import map

baseURL = "http://127.0.0.1:8000/"

def getUser(userID: int) -> dict:
    """
        Gets a user from the Database

        :param userID: The ID of the user to get
        :return: A dictionary containing the user's information
    """

    data = {
        "userID": userID
    }
    path = "user/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def postUser(name: str, email: str, phone: str, password: str) -> dict:
    """
        Creates a new user in the Database

        :param name: The name of the user
        :param email: The email of the user
        :param phone: The phone number of the user
        :param password: The password of the user
        :return: A dictionary containing the user's information
    """
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }
    path = "user/"
    response = requests.post(url=baseURL+path, json=data)
    if response.status_code==201:
        return response.json()
    return requests.exceptions.HTTPError

def deleteUser(userID: int) -> dict:
    """
        Deletes a user from the Database

        :param userID: The ID of the user to delete    
        :return: A dictionary containing the user's information
    """
    data = {
        "userID": userID
    }
    path = "user/"
    response = requests.delete(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def getDriver(driverID: int) -> dict:
    """
        Gets a driver from the Database
        
        :param driverID: The ID of the driver to get
        :return: A dictionary containing the driver's information
    """

    data = {
        "driverID": driverID
    }
    path = "driver/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def postDriver(name: str, email: str, phone: str, password:str, latitude: float, longitude:float, vehicle_type: str, rating: float, available: bool) -> dict:
    """
        Creates a driver in the Database

        :param name: The name of the driver
        :param email: The email of the driver
        :param phone: The phone number of the driver
        :param password: The password of the driver
        :param latitude: The latitude of the driver
        :param longitude: The longitude of the driver
        :param vehicle_type: The type of vehicle the driver has
        :param rating: The rating of the driver
        :param available: Whether the driver is available or not
        :return: A dictionary containing the driver's information
    """
    data = {
        "name" : name,
        "email" : email,
        "phone" : phone,
        "password" : password,
        "latitude" : latitude,
        "longitude" : longitude,
        "vehicle_type" : vehicle_type,
        "rating" : rating,
        "available" : available
    }
    path = "driver/"
    response = requests.post(url=baseURL+path, json=data)
    if response.status_code==201:
        return response.json()
    return requests.exceptions.HTTPError

def deleteDriver(driverID: int) -> dict:
    """
        Deletes a driver from the Database

        :param driverID: The ID of the driver to be deleted
        :return: A dictionary containing the driver's information
    """
    data = {
        "driverID": driverID
    }
    path = "driver/"
    response = requests.delete(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.InvalidJSONError

def getRide(rideID: int) -> dict:
    """
        Gets a ride from the Database

        :param rideID: The ID of the ride to be retrieved
        :return: A dictionary containing the ride's information
    """
    data = {
        "rideID": rideID
    }
    path = "ride/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def postRide(userID: int, driverID: int, start_lat:float, start_long: float, end_lat: float, end_long:float, advanced_booking:bool, price: float) -> dict:
    """
        Creates a ride in the Database

        :param userID: The ID of the user who is requesting the ride
        :param driverID: The ID of the driver who is providing the ride
        :param start_lat: The starting latitude of the ride
        :param start_long: The starting longitude of the ride
        :param end_lat: The ending latitude of the ride
        :param end_long: The ending longitude of the ride
        :param advanced_booking: Whether the ride is an advanced booking or not
        :param price: The price of the ride
        :return: A dictionary containing the ride's information
    """
    data = {
        "userID": userID,
        "driverID": driverID,
        "start_lat": start_lat,
        "start_long": start_long,
        "end_lat": end_lat,
        "end_long": end_long,
        "advanced_booking": advanced_booking,
        "price": price
    }
    path = "ride/"
    response = requests.post(url=baseURL+path, json=data)
    if response.status_code==201:
        return response.json()
    return requests.exceptions.HTTPError

def deleteRide(rideID) -> dict:
    """
        Deletes a ride from the Database

        :param rideID: The ID of the ride to be deleted
        :return: A dictionary containing the ride's information
    """
    data = {
        "rideID": rideID
    }
    path = "ride/"
    response = requests.delete(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def startUser(email, password) -> dict:
    """
        Starts a user session in login page

        :param email: The email of the user
        :param password: The password of the user
        :return: A dictionary containing the user's information
    """

    data = {
        "email": email,
        "password": password
    }
    path = "user/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def nearestDrivers(latitude, longitude, vehicle_type):
    """
        Returns the 5 nearest drivers to the user

        :param latitude: The latitude of the user
        :param longitude: The longitude of the user
        :param vehicle_type: The type of vehicle the user wants to ride
        :return: A list of dictionaries containing the drivers' information
    """
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "vehicle_type": vehicle_type
    }
    path = "ride_request/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def getTop5NearestDrivers(latitude, longitude, vehicle_type):
    """
        Returns the top 5 nearest drivers to the user after calculating through MAPBOX API

        :param latitude: The latitude of the user
        :param longitude: The longitude of the user
        :param vehicle_type: The type of vehicle the user wants to ride
        :return: A list of dictionaries containing the drivers' information
    """
    nearbyDrivers = nearestDrivers(latitude, longitude, vehicle_type)
    api = map.API()
    calculated = {}
    for driver in nearbyDrivers:
        result = api.get_details(driver['latitude'], driver['longitude'], latitude, longitude)
        if result != None:
            time= result[0]
            calculated[driver['driverID']] = time/driver['rating']
    calculated = sorted(calculated.items(), key=lambda item: item[1])
    return calculated


# print(postDriver("Subash", "abc@gmail.com", "12345", "123", 13.22, 80.24, "car", 4.8, True))
# print()
# print(postUser("Sub", "123@gmail.com", "4560", "100"))
# print()
# print(postRide(1, 1, 13.45, 80.24, 13.54, 80.43, False, 450))

print(startUser("123@gmail.com", "100"))