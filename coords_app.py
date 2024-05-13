from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import gps
from kivy.uix.button import Button

class GPSApp(App):
    def build(self):
        self.label = Label(text="Latitude: \nLongitude: ")
        self.start_gps()
        self.b1= Button(text= 'get gps', on_release= self.on_location)
        return self.label

    def start_gps(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except NotImplementedError:
            self.label.text = "GPS is not available on your platform"

    def on_location(self, **kwargs):
        latitude = kwargs.get('lat')
        longitude = kwargs.get('lon')
        if latitude is not None and longitude is not None:
            self.label.text = f"Latitude:{latitude} \nLongitude:{longitude} "
            Clock.schedule_once(lambda dt: self.update_label(latitude, longitude))

    def update_label(self, latitude, longitude):
        self.label.text = f"Latitude: {latitude}\nLongitude: {longitude}"

    def on_stop(self):
        gps.stop()

if __name__ == '__main__':
    GPSApp().run()
