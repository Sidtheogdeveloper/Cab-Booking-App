import datetime

def money_gen(distance, base, dbase,type):
    if distance <= 2.5 and distance > 0:
        if (type == 'bike'):
            basicfare = 20
        elif (type == 'auto'):
            basicfare = 40
        elif (type == 'prime sedan'):
            basicfare = 100
        elif (type == 'suv'):
            basicfare = 130
    elif distance <= 20:
        basicfare = round(distance * base,2)
    else:
        basicfare = round((20 * base) + (distance - 20) * dbase,2)
    
    gst = round(18 / 100 * basicfare,2)
    confee = round(1 / 100 * basicfare,2)
    insurance = round(1 / 100 * basicfare,2)
    total = round(basicfare + gst + confee + insurance, 2)
    
    return basicfare, gst, confee, insurance, total

def price_gen(distance, type):
    current_time = datetime.datetime.now().time()
    if current_time.hour >= 6 and current_time.hour < 12 and type == 'prime sedan':
        return money_gen(distance, 18, 16,type)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'prime sedan':
        return money_gen(distance, 19, 18.5,type)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'prime sedan':
        return money_gen(distance, 18.75, 18,type)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'prime sedan':
        return money_gen(distance, 18, 16,type)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'prime sedan':
        return money_gen(distance, 19, 18,type)
    elif current_time.hour >= 21 and current_time.hour < 0 and type == 'prime sedan':
        return money_gen(distance, 21.5, 20,type)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'prime sedan':
        return money_gen(distance, 23.5, 22,type)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'suv':
        return money_gen(distance, 36, 34,type)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'suv':
        return money_gen(distance, 40, 38.5,type)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'suv':
        return money_gen(distance, 38, 37.5,type)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'suv':
        return money_gen(distance, 36, 34,type)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'suv':
        return money_gen(distance, 38, 36,type)
    elif current_time.hour >= 21 and current_time.hour < 0 and type == 'suv':
        return money_gen(distance, 44, 43.5,type)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'suv':
        return money_gen(distance, 48, 47,type)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'auto':
        return money_gen(distance, 6, 5,type)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'auto':
        return money_gen(distance, 7, 6,type)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'auto':
        return money_gen(distance, 9, 8.5,type)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'auto':
        return money_gen(distance, 7, 6.5,type)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'auto':
        return money_gen(distance, 9, 8,type)
    elif current_time.hour >= 21 and current_time.hour < 0 and type == 'auto':
        return money_gen(distance, 10, 9.5,type)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'auto':
        return money_gen(distance, 13, 11.5,type)
    elif current_time.hour >= 6 and current_time.hour < 12 and type == 'bike':
        return money_gen(distance, 5, 3.5,type)
    elif current_time.hour >= 12 and current_time.hour < 14 and type == 'bike':
        return money_gen(distance, 5, 4.8,type)
    elif current_time.hour >= 14 and current_time.hour < 17 and type == 'bike':
        return money_gen(distance, 7, 6.5,type)
    elif current_time.hour >= 17 and current_time.hour < 20 and type == 'bike':
        return money_gen(distance, 6, 5.5,type)
    elif current_time.hour >= 20 and current_time.hour < 21 and type == 'bike':
        return money_gen(distance, 8, 7,type)
    elif current_time.hour >= 21 and current_time.hour < 0 and type == 'bike':
        return money_gen(distance, 8, 8,type)
    elif current_time.hour >= 0 and current_time.hour < 6 and type == 'bike':
        return money_gen(distance, 11, 10,type)
    

def adv_price_gen(distance, type, input_time):
    current_time = datetime.datetime.now().time()
    current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)
    input_datetime = datetime.datetime.combine(datetime.date.today(), input_time)
    
    if input_datetime > current_datetime:
        time_diff_minutes = (input_datetime - current_datetime).total_seconds() / 60

        if time_diff_minutes < 5:
            advance_charge = {'auto': 50, 'prime sedan': 60, 'suv': 100, 'bike': 25}[type]
        elif 5 <= time_diff_minutes < 15:
            advance_charge = {'auto': 70, 'prime sedan': 60, 'suv': 120, 'bike': 35}[type]
        elif 15 <= time_diff_minutes < 20:
            advance_charge = {'auto': 75, 'prime sedan': 65, 'suv': 130, 'bike': 30}[type]
        elif 20 <= time_diff_minutes < 24 * 60:
            advance_charge = {'auto': 80, 'prime sedan': 70, 'suv': 140, 'bike': 40}[type]

        basicfare, gst, confee, insurance, total = price_gen(distance, type)
        total_with_advance = total + advance_charge

        return advance_charge, basicfare, gst, confee, insurance, total_with_advance
    else:
        basicfare, gst, confee, insurance, total = price_gen(distance, type)
        return 0, basicfare, gst, confee, insurance, total

    



    
    
    
    
if __name__ == '__main__':
    distance = 1
    type = 'suv'
    basicfare, gst, confee, insurance, total = price_gen(distance, type)
    print(f"Basic Fare: Rs. {basicfare}, GST: Rs. {gst}, Convenience Fee: Rs. {confee}, Insurance: Rs. {insurance}, Total: Rs. {total}")
