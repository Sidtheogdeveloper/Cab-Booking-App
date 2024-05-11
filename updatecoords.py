from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import gps
import sqlite3

# Database setup
conn = sqlite3.connect('driver_db.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY,
                    latitude REAL,
                    longitude REAL
                  )''')
conn.commit()

# Function to update database with coordinates
def update_database(**kwargs):
    lat = kwargs.get('lat')
    lon = kwargs.get('lon')
    # Update database with new coordinates
    cursor.execute('UPDATE drivers SET latitude=?, longitude=? WHERE id=1', (lat, lon))
    conn.commit()

# Kivy App for continuously updating driver coordinates
class DriverCoordinatesUpdaterApp(App):
    def build(self):
        # Schedule the update_coordinates method to be called every 5 seconds
        Clock.schedule_interval(self.update_coordinates, 5)
        return Label(text="Driver coordinates updater started. Press Ctrl+C to exit.")

    # Function to get GPS coordinates using Plyer
    def get_coordinates(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except NotImplementedError:
            print('GPS is not available on your platform')

    # Callback function for Plyer GPS location updates
    def on_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if lat is not None and lon is not None:
            update_database(lat=lat, lon=lon)

    # Function to continuously update coordinates
    def update_coordinates(self, dt):
        self.get_coordinates()

# Run the Kivy App
if __name__ == "__main__":
    DriverCoordinatesUpdaterApp().run()
