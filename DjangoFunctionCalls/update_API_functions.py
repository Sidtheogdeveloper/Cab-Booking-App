import requests, requests.exceptions
# import datetime

#baseURL = "http://127.0.0.1:8000/"
baseURL= "http://192.168.168.12:8000/"

def updateUserPassword(userID: int, newPassword: str) -> dict:
    """
        Updates the password of a user with the given userID to the given newPassword.

        :param userID: The ID of the user to update.
        :param newPassword: The new password of the user.
        :return: A dictionary with the details of the user.
    """
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
    """
        Updates the password of a driver with the given driverID to the given newPassword.

        :param driverID: The ID of the driver to update
        :param newPassword: The new password of the driver
        :return: A dictionary with the details of the driver.
    """
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
    """
        Updates the coordinates of a driver with the given driverID to the given newLatitude and newLongitude.

        :param driverID: The ID of the driver to update
        :param newLatitude: The new latitude of the driver
        :param newLongitude: The new longitude of the driver
        :return: A dictionary with the details of the driver.
    """
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
    """
        Updates the availability of a driver with the given driverID to the given newAvailability.
        
        :params driverID: The ID of the driver to update
        :params newAvailability: The new availability of the driver
        :return: A dictionary with the details of the driver.
    """
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