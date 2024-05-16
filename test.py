from API_Functions import postDriver

drivers = [
    ["Raju", "abc@gmail.com", "1234567890", "asdfgf", "TN05 AK1234", 12.7226, 80.1889, "auto", 4.5, True],
    ["Ravi", "xyz@gmail.com", "9876543210", "qwerty", "TN61 WK1234", 12.6131, 80.1673, "sedan", 4.8, True],
    ["Rajesh", "pqr@gmail.com", "1234567890", "zxcvbn", "TN61 WK1234", 12.7906, 80.2218, "suv", 4.1, True],
    ["Ramesh", "lmn@gmail.com", "9876543210", "asdfgh", "TN61 WK1234", 12.8453, 80.2264, "bike", 4.0, True],
    ["John Doe", "john.doe@example.com", "1234567890", "password123", "TN01 AB1234", 12.8586, 80.1997, "auto", 4.5, True],
    ["Jane Smith", "jane.smith@example.com", "2345678901", "password456", "TN02 CD5678", 12.8483, 80.2075, "sedan", 4.8, True],
    ["Michael Johnson", "michael.johnson@example.com", "3456789012", "password789", "TN03 EF9012", 12.8582, 80.2264, "suv", 4.1, True],
    ["Amanda Brown", "amanda.brown@example.com", "4567890123", "passwordabc", "TN04 GH3456", 12.8533, 80.2416, "bike", 4.0, True],
    ["William Wilson", "william.wilson@example.com", "5678901234", "passworddef", "TN05 IJ7890", 12.7709, 80.2130, "auto", 4.2, True],
    ["Emma Taylor", "emma.taylor@example.com", "6789012345", "passwordegf", "TN06 KL2345", 12.7842, 80.2173, "sedan", 4.6, True],
    ["Matthew Anderson", "matthew.anderson@example.com", "7890123456", "passwordhij", "TN07 MN4567", 12.7860, 80.2202, "suv", 4.9, True],
    ["Olivia Martinez", "olivia.martinez@example.com", "8901234567", "passwordklm", "TN08 OP6789", 12.7837, 80.2236, "bike", 4.3, True],
    ["Ethan Wilson", "ethan.wilson@example.com", "9012345678", "passwordnop", "TN09 QR7890", 12.7735, 80.2146, "auto", 4.7, True],
    ["Sophia Thomas", "sophia.thomas@example.com", "0123456789", "passwordqrs", "TN10 ST8901", 12.8421, 80.1510, "sedan", 4.0, True],
    ["Alexander Garcia", "alexander.garcia@example.com", "1123456789", "passwordtuv", "TN11 UV2345", 12.8327, 80.1591, "suv", 4.5, True],
    ["Isabella Rodriguez", "isabella.rodriguez@example.com", "2123456789", "passwordwxy", "TN12 WX4567", 12.8393, 80.1537, "bike", 4.8, True],
    ["James Martinez", "james.martinez@example.com", "3123456789", "passwordzab", "TN13 YZ6789", 12.8852, 80.0815, "auto", 4.1, True],
    ["Amelia Smith", "amelia.smith@example.com", "4123456789", "password123", "TN14 AB1234", 12.8778, 80.0799, "sedan", 4.4, True],
    ["Benjamin Johnson", "benjamin.johnson@example.com", "5123456789", "password456", "TN15 CD5678", 12.8968, 80.0839, "suv", 4.2, True],
    ["Charlotte Brown", "charlotte.brown@example.com", "6123456789", "password789", "TN16 EF9012", 12.8927, 80.0859, "bike", 4.9, True],
    ["Daniel Wilson", "daniel.wilson@example.com", "7123456789", "passwordabc", "TN17 GH3456", 12.8935, 80.0811, "auto", 4.5, True],
]

for driver in drivers:
    postDriver(*driver)