import datetime
import map
from API_Functions import getTop5NearestDrivers, getDriver

def money_gen(distance, base, dbase):
    if distance <= 20:
        basicfare = round(distance * base,2)
    else:
        basicfare = round((20 * base) + (distance - 20) * dbase,2)
    
    gst = round(18 / 100 * basicfare,2)
    confee = round(1 / 100 * basicfare,2)
    insurance = round(1 / 100 * basicfare,2)
    total = round(basicfare + gst + confee + insurance, 2)
    
    return (basicfare, gst, confee, insurance, total)

def price_gen(distance, type):
    distance = distance/1000
    current_time = datetime.datetime.now().time()
    if current_time.hour >= 6 and current_time.hour < 12 and type == 'sedan':
        return money_gen(distance, 20, 18)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'sedan':
        return money_gen(distance, 21, 20.5)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'sedan':
        return money_gen(distance, 20.75, 20)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'sedan':
        return money_gen(distance, 20, 18)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'sedan':
        return money_gen(distance, 21, 20)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'sedan':
        return money_gen(distance, 23.5, 22)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'sedan':
        return money_gen(distance, 30.5, 29)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'suv':
        return money_gen(distance, 38, 36)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'suv':
        return money_gen(distance, 42, 40.5)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'suv':
        return money_gen(distance, 40, 39.5)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'suv':
        return money_gen(distance, 38, 36)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'suv':
        return money_gen(distance, 40, 38)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'suv':
        return money_gen(distance, 46, 45.5)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'suv':
        return money_gen(distance, 54, 53)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'auto':
        return money_gen(distance, 8, 7)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'auto':
        return money_gen(distance, 9, 8)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'auto':
        return money_gen(distance, 11, 10.5)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'auto':
        return money_gen(distance, 9, 8.5)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'auto':
        return money_gen(distance, 11, 10)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'auto':
        return money_gen(distance, 12, 11.5)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'auto':
        return money_gen(distance, 18, 16.5)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'bike':
        return money_gen(distance, 7, 5.5)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'bike':
        return money_gen(distance, 7, 6.8)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'bike':
        return money_gen(distance, 9, 8.5)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'bike':
        return money_gen(distance, 8, 7.5)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'bike':
        return money_gen(distance, 10, 9)
    elif current_time.hour >= 21 and current_time.hour < 24 and type == 'bike':
        return money_gen(distance, 10, 10)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'bike':
        return money_gen(distance, 13, 12)
    else: 
        return "ERROR"
    

def adv_price_gen(distance, type, date: str, time: str):
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
    



# details = something.book_now(lat1, lon1, lat2, lon2, vehicle_type)
# details = something.book_advanced(lat1, lon1, lat2, lon2, vehicle_type, date, time)

def book_now(lat1, lon1, lat2, lon2, vehicle_type):
    myMap = map.API()
    time, distance = myMap.get_details(lat1, lon1, lat2, lon2)
    basicfare, gst, confee, insurance, total = price_gen(distance, vehicle_type)
    nearestDriver = getTop5NearestDrivers(lat1, lon1, vehicle_type)
    time_to_arrive = nearestDriver[0][1][1]
    driver_details = getDriver(nearestDriver[0][0])
    details = {
        "price": total,
        "driver_name": driver_details["name"],
        "vehicle_number": driver_details["vehicle_number"],
        "otp": 1234,
        "basic": basicfare,
        "gst": gst,
        "convenience": confee,
        "insurance": insurance,
        "time_of_travel": time,            # Time to travel from pickup to destination point
        "time_to_arrive": time_to_arrive   # Time for the driver to arrive to the pickup point
    }
    return details

def book_advanced(lat1, lon1, lat2, lon2, vehicle_type, date, times):
    myMap = map.API()
    time, distance = myMap.get_details(lat1, lon1, lat2, lon2)
    advance_charge, basicfare, gst, confee, insurance, total_with_advance = adv_price_gen(distance, vehicle_type, date, times)
    nearestDriver = getTop5NearestDrivers(lat1, lon1, vehicle_type)
    time_to_arrive = nearestDriver[0][1][1]
    driver_details = getDriver(nearestDriver[0][0])
    details = {
        "price": total_with_advance,
        "driver_name": driver_details["name"],
        "vehicle_number": driver_details["vehicle_number"], 
        "otp": 1234,
        "basic": basicfare,
        "gst": gst,
        "convenience": confee,
        "insurance": insurance,
        "advance": advance_charge,
        "time_of_travel": time,            # Time to travel from pickup to destination point
        "time_to_arrive": time_to_arrive   # Time for the driver to arrive to the pickup point
    }
    return details
    
# print(adv_price_gen(10000, 'sedan', '16-05-24', '18:00'))
# print(price_gen(10000, 'suv'))
