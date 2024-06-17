import requests, requests.exceptions
import map

baseURL = "http://127.0.0.1:8000/"
#baseURL= "http://10.106.175.77:8000/"

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
    return "error"

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

def postDriver(name: str, email: str, phone: str, password:str, vehicle_number: str, latitude: float, longitude:float, vehicle_type: str, rating: float, available: bool, no_of_ratings: int) -> dict:
    """
        Creates a driver in the Database

        :param name: The name of the driver
        :param email: The email of the driver
        :param phone: The phone number of the driver
        :param password: The password of the driver
        :param vehicle_number: The vehicle number of the driver
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
        "vehicle_number": vehicle_number,
        "latitude" : latitude,
        "longitude" : longitude,
        "vehicle_type" : vehicle_type,
        "rating" : rating,
        "available" : available,
        "no_of_ratings": no_of_ratings
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

def postRide(userID: int, driverID: int, start_lat:float, start_long: float, end_lat: float, end_long:float, advanced_booking:bool, price: float, status: str) -> dict:
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
        "price": price,
        "status": status
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
    return "error"


def forgotUser(email) -> dict:
    """
        Starts a user session in login page

        :param email: The email of the user
        :param password: The password of the user
        :return: A dictionary containing the user's information
    """

    data = {
        "email": email
    }
    path = "user/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return "error"

def giveRatings(driverID: int, rating: float):
    data = {
        "driverID": driverID,
        "rating": rating
    }
    path = "driver/"
    response = requests.put(url=baseURL+path, json=data)
    if response.status_code==200:
        return response.json()

def completeRide(rideID: int):
    data = {
        "rideID": rideID
    }
    path = "ride/"
    response = requests.put(url=baseURL+path, json=data)
    if response.status_code==200:
        return response.json()

def getRidesOfUsers(userID: int):
    """
        Gets all the rides of a user
        :param userID: The ID of the user
        :return: A list of dictionaries containing the rides of the user
    """
    Data = {
        "userID": userID
    }
    path = "ride/"
    response = requests.get(url=baseURL+path, params=Data)
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
            calculated[driver['driverID']] = time/driver['rating'], time
    calculated = sorted(calculated.items(), key=lambda item: item[1][0])
    return calculated

def get_address(lat, lon):
    apikey= "pk.eyJ1Ijoic2lkZGhhcnRoMTciLCJhIjoiY2x2ZXA0ODN2MDR4azJqbjUyZGQ4ZGd2ZSJ9.rJCQ3lzhBFyHLEJWe9mLjQ"
    query= f"https://api.mapbox.com/search/geocode/v6/reverse?longitude={lon}&latitude={lat}&access_token={apikey}"
    #To get the address of that location
    res= requests.get(query)
    address_info= res.json()
    address= address_info['features'][0]['properties']['full_address']
    return(address)

def route(start_lat, end_lat, start_lon, end_lon):
    apikey= "pk.eyJ1Ijoic2lkZGhhcnRoMTciLCJhIjoiY2x2ZXA0ODN2MDR4azJqbjUyZGQ4ZGd2ZSJ9.rJCQ3lzhBFyHLEJWe9mLjQ"
    url= f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_lon}%2C{start_lat}%3B{end_lon}%2C{end_lat}?alternatives=true&geometries=geojson&language=en&overview=full&steps=true&access_token={apikey}"
    res= requests.get(url)
    routes= res.json()
    try:
        return routes['routes'][0]['geometry']['coordinates']
    except IndexError:
        return []

def distance_time(start_lat, end_lat, start_lon, end_lon):
    apikey= "pk.eyJ1Ijoic2lkZGhhcnRoMTciLCJhIjoiY2x2ZXA0ODN2MDR4azJqbjUyZGQ4ZGd2ZSJ9.rJCQ3lzhBFyHLEJWe9mLjQ"
    url= f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_lon}%2C{start_lat}%3B{end_lon}%2C{end_lat}?alternatives=true&geometries=geojson&language=en&overview=full&steps=true&access_token={apikey}"
    res= requests.get(url)
    routes= res.json()
    try:
        distance= routes['routes'][0]['legs'][0]['distance']//1000
        time= routes['routes'][0]['legs'][0]['duration']//60
        return {'distance': distance, 'time': time}
    except IndexError:
        return []


#print(getTop5NearestDrivers(13.22, 18.22, 'auto'))
#print(distance_time(12.963045, 12.751801, 80.155388, 80.195878))
# print(postDriver("Subash", "abc@gmail.com", "12345", "123", "TN05 BE4392", 13.22, 80.24, "car", 4.8, True))
# # print()
# # print(postUser("Sub", "123@gmail.com", "4560", "100"))
# # print()
#print(postRide(1, 1, 13.45, 80.24, 13.54, 80.43, True, 450))
# #print(startUser("123@gmail.com", "100"))
#print(get_address(13.0827, 80.2707))
#print(getDriver(56))
#print(getRide(2))
#print(getDriver(25))
