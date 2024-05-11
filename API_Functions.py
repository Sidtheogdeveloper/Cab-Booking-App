import requests, requests.exceptions
import map

baseURL = "http://127.0.0.1:8000/"

def getUser(userID: int):
    data = {
        "userID": userID
    }
    path = "user/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def postUser(name: str, email: str, phone: str, password: str):
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

def deleteUser(userID: int):
    data = {
        "userID": userID
    }
    path = "user/"
    response = requests.delete(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def getDriver(driverID: int):
    data = {
        "driverID": driverID
    }
    path = "driver/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def postDriver(name: str, email: str, phone: str, password:str, latitude: float, longitude:float, vehicle_type: str, rating: float, available: bool):
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

def deleteDriver(driverID: int):
    data = {
        "driverID": driverID
    }
    path = "driver/"
    response = requests.delete(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.InvalidJSONError

def getRide(rideID: int):
    data = {
        "rideID": rideID
    }
    path = "ride/"
    response = requests.get(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def postRide(userID: int, driverID: int, start_lat:float, start_long: float, end_lat: float, end_long:float, advanced_booking:bool, price: float):
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

def deleteRide(rideID):
    data = {
        "rideID": rideID
    }
    path = "ride/"
    response = requests.delete(url=baseURL+path, params=data)
    if response.status_code==200:
        return response.json()
    return requests.exceptions.HTTPError

def nearestDrivers(latitude, longitude, vehicle_type):
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
# print(postUser("Raj", "xyz@gmail.com", "4567", "345"))
# print()
# print(postRide(1, 1, 13.45, 80.24, 13.54, 80.43, False, 450))


