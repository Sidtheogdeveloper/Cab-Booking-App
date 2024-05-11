import requests, requests.exceptions
# import datetime

baseURL = "http://127.0.0.1:8000/"

def updateUserPassword(userID: int, newPassword: str):
    Data = {
        "userID": userID,
        "password": newPassword
    }
    path = "user/"
    response = requests.put(url=baseURL+path, data=Data)
    if response.status_code == 200:
        return response.json()
    return requests.exceptions.HTTPError

def updateDriverPassword(driverID: int, newPassword: str):
    Data = {
        "driverID": driverID,
        "password": newPassword
    }
    path = "driver/"
    response = requests.put(url=baseURL+path, data=Data)
    if response.status_code == 200:
        return response.json()
    return requests.exceptions.HTTPError

def updateDriverCoordinates(driverID: int, newLatitude: float, newLongitude: float):
    Data = {
        "driverID": driverID,
        "latitude": newLatitude,
        "longitude": newLongitude
    }
    path = "driver/"
    response = requests.put(url=baseURL+path, data=Data)
    if response.status_code == 200:
        return response.json()
    return requests.exceptions.HTTPError

def updateDriverAvailability(driverID: int, newAvailability: bool):
    Data = {
        "driverID": driverID,
        "available": newAvailability
    }
    path = "driver/"
    response = requests.put(url=baseURL+path, data=Data)
    if response.status_code == 200:
        return response.json()
    return requests.exceptions.HTTPError

# def processRideRequest(userID: int, pickupLatitude: float, pickupLongitude: float, vehicle_type: str, advancedBooking: bool, time: int, price: int):
#     bestDrivers = API_Functions.nearestDrivers(pickupLatitude, pickupLongitude, vehicle_type)
#     for driver in bestDrivers:
#                           # driverID
#         if (driverResponse(driver[0], price, time)):
#             return API_Functions.getDriver(driver[0])
#     return requests.exceptions.RetryError


# print(updateUserPassword(3, "000"))