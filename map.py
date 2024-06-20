import requests
from urllib.parse import quote

class API():
    apiKey = "pk.eyJ1Ijoic2lkZGhhcnRoMTciLCJhIjoiY2x2ZXA0ODN2MDR4azJqbjUyZGQ4ZGd2ZSJ9.rJCQ3lzhBFyHLEJWe9mLjQ"

    def get_image(self, lon1, lat1, lon2, lat2, geometry):
        geometry = quote(geometry, safe="")
        url = "https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/pin-s+ff0000(" + str(lon1) + "," + str(lat1) + "),pin-s+ff0000(" + str(lon2) + "," + str(lat2) + "),path+3734fe(" + geometry + ")/auto/300x200?padding=50&access_token=" + self.apiKey

        image = requests.get(url)
        if image.status_code == 200:
            with open('map_image_new.png', 'wb') as f:
                f.write(image.content)
            print("Image saved successfully.")
        else:
            print("Error:", image.status_code)

    def get_details(self, lat1, lon1, lat2, lon2):
        data = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/driving/{lon1}%2C{lat1}%3B{lon2}%2C{lat2}?alternatives=true&geometries=polyline&language=en&overview=full&steps=true&access_token={self.apiKey}")
        if data.status_code == 200:
            try:
                ride_data = data.json()["routes"][0]
                result = [ride_data["duration"], ride_data["distance"], ride_data["geometry"]]
                return (result[:2])
            except IndexError:
                return None
        else:
            print("Error:", data.status_code)

    def searchResults(self, prompt):
        url = f'https://api.mapbox.com/search/searchbox/v1/suggest?q={prompt.replace(" ", "+")}&language=en&session_token=0d4b3ce0-00d6-4ed1-88f3-79cb215076b5&access_token={self.apiKey}'
        results = requests.get(url)
        if results.status_code == 200:
            results = results.json()["suggestions"]
            suggestions = [[result["name"], result["mapbox_id"]] for result in results]
            return suggestions

    def suggestionCoordinates(self, prompt):
        suggestions = self.searchResults(prompt)
        if not suggestions:
            return IndexError
        for suggestion in suggestions:
            coords = requests.get(f"https://api.mapbox.com/search/searchbox/v1/retrieve/{suggestion[1]}?session_token=0d4b3ce0-00d6-4ed1-88f3-79cb215076b5&access_token={self.apiKey}")
            suggestion[1] = coords.json()["features"][0]["geometry"]["coordinates"]
        return suggestions