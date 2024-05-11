import requests

url = 'http://127.0.0.1:8000//assigner/add/'
data = {
    'id': 8,
    'available': True,
    'latitude': 13.93,
    'longitude': 81.05,
    'vehicle_type': 'car'
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.json())