import requests

apiKey = "pk.eyJ1Ijoic2lkZGhhcnRoMTciLCJhIjoiY2x2ZXBhdm1lMDk1ZzJqbmpxZHJuMzNrOCJ9.EFJgFVLpWcw6na48RwJN-g"

image = requests.get(f"https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/80.2639,13.0835,12.34,0/300x200?access_token={apiKey}")

if image.status_code == 200:
    with open('map_image.png', 'wb') as f:
        f.write(image.content)
    print("Image saved successfully.")
else:
    print("Error:", image.status_code)
