import datetime
import map, random
from API_Functions import getTop5NearestDrivers, getDriver, deleteRide, getRide


def money_gen(distance, base, dbase):
    if distance <= 20:
        basicfare = round(distance * base,2)
    else:
        basicfare = round((20 * base) + (distance - 20) * dbase,2)
    
    gst = round(18 / 100 * basicfare,2)
    confee = round(1 / 100 * basicfare,2)
    insurance = round(1 / 100 * basicfare,2)
    total = round(basicfare + gst + confee + insurance)
    
    return (basicfare, gst, confee, insurance, total)

def price_gen(distance, type):
    distance = distance/1000
    current_time = datetime.datetime.now().time()
    if current_time.hour >= 6 and current_time.hour < 12 and type == 'sedan':
        return money_gen(distance, 18, 16)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'sedan':
        return money_gen(distance, 19, 18.5)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'sedan':
        return money_gen(distance, 18.75, 18)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'sedan':
        return money_gen(distance, 18, 16)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'sedan':
        return money_gen(distance, 19, 18)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'sedan':
        return money_gen(distance, 21.5, 20)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'sedan':
        return money_gen(distance, 23.5, 22)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'suv':
        return money_gen(distance, 36, 34)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'suv':
        return money_gen(distance, 40, 38.5)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'suv':
        return money_gen(distance, 38, 37.5)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'suv':
        return money_gen(distance, 36, 34)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'suv':
        return money_gen(distance, 38, 36)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'suv':
        return money_gen(distance, 44, 43.5)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'suv':
        return money_gen(distance, 48, 47)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'auto':
        return money_gen(distance, 6, 5)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'auto':
        return money_gen(distance, 7, 6)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'auto':
        return money_gen(distance, 9, 8.5)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'auto':
        return money_gen(distance, 7, 6.5)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'auto':
        return money_gen(distance, 9, 8)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'auto':
        return money_gen(distance, 10, 9.5)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'auto':
        return money_gen(distance, 13, 11.5)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'bike':
        return money_gen(distance, 5, 3.5)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'bike':
        return money_gen(distance, 5, 4.8)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'bike':
        return money_gen(distance, 7, 6.5)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'bike':
        return money_gen(distance, 6, 5.5)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'bike':
        return money_gen(distance, 8, 7)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'bike':
        return money_gen(distance, 8, 8)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'bike':
        return money_gen(distance, 11, 10)
    else: 
        return "ERROR"
    

def adv_price_gen(distance, type, date, time):
    current_datetime = datetime.datetime.now()
    input_datetime = datetime.datetime.strptime(date + " " + time, "%d-%m-%y %H:%M")
    if input_datetime > current_datetime:
        time_diff_minutes = (input_datetime - current_datetime).total_seconds() / 60
        if time_diff_minutes < 30:
            advance_charge = {'auto': 50, 'sedan': 60, 'suv': 100, 'bike': 25}[type]
        elif 30 <= time_diff_minutes < 60:
            advance_charge = {'auto': 70, 'sedan': 60, 'suv': 120, 'bike': 35}[type]
        elif 60 <= time_diff_minutes < 120:
            advance_charge = {'auto': 75, 'sedan': 65, 'suv': 130, 'bike': 30}[type]
        elif 120 <= time_diff_minutes < 24 * 60:
            advance_charge = {'auto': 80, 'sedan': 70, 'suv': 140, 'bike': 40}[type]
        else:
            return

        basicfare, gst, confee, insurance, total = price_gen(distance, type)
        total_with_advance = round(total + advance_charge)

        return advance_charge, basicfare, gst, confee, insurance, total_with_advance
    
def cancelRide(rideID):
    details = deleteRide(rideID)
    current_time = datetime.datetime.now()
    ride_time = datetime.datetime.strptime(details["date"] + ' ' + details["time"], '%Y-%m-%d %H:%M:%S.%f')
    time_difference = current_time - ride_time
    difference_in_minutes = time_difference.total_seconds() / 60
    if difference_in_minutes < 5:
        return 0
    elif 5 <= difference_in_minutes < 10:
        return 50
    else:
        return 100


def gen_otp():
    otp=''
    for i in range(4):
        val= '1234567890'
        nums= list(val)
        otp += random.choice(nums)
    return otp

# details = something.book_now(lat1, lon1, lat2, lon2, vehicle_type)
# details = something.book_advanced(lat1, lon1, lat2, lon2, vehicle_type, date, time)

def book_now(lat1, lon1, lat2, lon2, vehicle_type):
    myMap = map.API()
    duration, distance = myMap.get_details(lat1, lon1, lat2, lon2)[:2]
    basicfare, gst, confee, insurance, total = price_gen(distance, vehicle_type)
    driver = getTop5NearestDrivers(lat1, lon1, vehicle_type)[0]
    time_of_travel = driver[1][1]
    driver_details = getDriver(driver[0])
    print(driver_details)
    details = {
        "price": total,
        "driver_name": driver_details["name"],
        "driverID": driver_details['driverID'],
        "vehicle_number": driver_details["vehicle_number"],
        "phone": driver_details["phone"],
        "otp": gen_otp(),
        "basic": basicfare,
        "gst": gst,
        "convenience": confee,
        "insurance": insurance,
        "ride_distance": int(distance//1000),
        "duration": int(duration//60),
        "time_of_travel": int(time_of_travel//60)
    }
    return details

def book_advanced(lat1, lon1, lat2, lon2, vehicle_type, date, time):
    myMap = map.API()
    duration, distance = myMap.get_details(lat1, lon1, lat2, lon2)[:2]
    advance_charge, basicfare, gst, confee, insurance, total_with_advance = adv_price_gen(distance, vehicle_type, date, time)
    driver = getTop5NearestDrivers(lat1, lon1, vehicle_type)[0]
    time_of_travel = driver[1][1]
    driver_details = getDriver(driver[0])
    print(driver_details)
    details = {
        "price": total_with_advance,
        "driver_name": driver_details["name"],
        "driverID": driver_details['driverID'],
        "vehicle_number": driver_details["vehicle_number"], 
        "phone": driver_details["phone"],
        "otp": gen_otp(),
        "basic": basicfare,
        "gst": gst,
        "convenience": confee,
        "insurance": insurance,
        "advance": advance_charge,
        "ride_distance": int(distance//1000),
        "duration": int(duration//60),
        "time_of_travel": int(time_of_travel//60)
    }
    return details
    
# print(adv_price_gen(10000, 'sedan', '16-05-24', '18:00'))
# print(price_gen(10000, 'suv'))
# print(getRide(1))

def cancelRide(rideID):
    details = deleteRide(rideID)
    current_time = datetime.datetime.now()
    ride_time = datetime.datetime.strptime(details["date"] + ' ' + details["time"], '%Y-%m-%d %H:%M:%S.%f')
    time_difference = current_time - ride_time
    difference_in_minutes = time_difference.total_seconds() / 60
    if difference_in_minutes < 5:
        return 0
    elif 5 <= difference_in_minutes < 10:
        return 50
    else:
        return 100
