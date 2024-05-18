from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import csv, os
import auth
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview.view import MapView
from kivy_garden.mapview.view import MapMarker
from kivy.uix.dropdown import DropDown
import map
import API_Functions as db
import update_API_functions as update_db
import price_generation as priceGen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class MainScreen(Screen):
    pass

class PassMenu(DropDown):
    pass

class PassengerLog(Screen):
    def __recent__(self, widget1, widget2):
        if os.path.exists("recentPlogin.csv"):
            f= open('recentPlogin.csv', 'r')
            reader= csv.reader(f)
            add_= []
            for i in reader:
                add_.append(i)
            email= add_[0][0]
            pwd= add_[0][1]
            widget1.text= email
            widget2.text= pwd
        else:
            pass
    
    
    def __submit__(self, email, password, widget):
        check= db.startUser(email=email, password=password)
        check_mail= db.forgotUser(email= email)
        if check != "error":
            self.otp= auth.gen_otp()
            response= auth.mail(email, check['name'], self.otp)
            self.otp= '123'
            f= open("recentPlogin.csv", 'w')
            writer= csv.writer(f)
            writer.writerow([email, password, check['userID']])
            f.close()
            if response== "error":
                widget.text= "Some Error occurred"
            else:
                widget.text="OTP sent to your Mail"
        elif check=='error' and check_mail!='error':
            widget.text= 'Incorrect Password'
        else:
            widget.text= 'Email does not exist'

    def __verify__(self, otp, widget):  
        if self.otp==otp:
            widget.text= 'OTP Verified'
            self.manager.current ='Phome'
        else:
            widget.text= 'Incorrect OTP'

class PassengerSP(Screen):
    def __enter_data__(self, name, phone, email,pwd ,cpwd, widget):  
        
        if pwd==cpwd:
            insert= db.postUser(name, email ,phone, pwd)
            if insert=='error':
                widget.text= 'email or phone already exists'
            else:
                self.otp= auth.gen_otp()
                auth.mail(email, name, self.otp)
                widget.text= "OTP Sent to your Email ID"

    def verify_otp(self, otp, widget):
        if  otp == self.otp:
            widget.text= "OTP verified"
        else:
            widget.text= 'Invalid OTP'

class ForgotpwdPas(Screen):
    def __verify__(self, email, widget):
        check= db.forgotUser(email)
        if check=='error':
            widget.text= "Email doesn't exist"
        else:
            self.otp= auth.gen_otp()
            auth.pwd_change_req(email,check['name'], self.otp)
            self.email= email
            self.user_id= check['userID']
            widget.text= 'OTP sent to you mail'
    
    def change_pwd(self, otp, widget):
        if self.otp==otp:
            with open('fppass.csv', 'w',newline= '') as f:
                writer= csv.writer(f)
                writer.writerow([self.user_id,self.email])
            self.manager.current= 'chpwdps'
        else:
            widget.text= 'Incorrect OTP'

class PassengerScreen(Screen):
    pass

class ChpwdPass(Screen):
    def _check_pwd_(self, npwd, cpwd, widget):
        if npwd!=cpwd:
            widget.text= "Passwords does't match"
        else:
            widget.text= 'Good to go'
    def _submit_(self, newpwd, cpwd, widget):
        if newpwd==cpwd:
            p= open('fppass.csv','r')
            pw= csv.reader(p)
            for i in pw:
                user_id= i[0]
                email= i[1]
            p.close()
            check= update_db.updateUserPassword(userID= user_id, newPassword= newpwd)
            data= db.getUser(user_id)
            auth.pwd_reset_info(email, data['name'])
            widget.text= 'Password Updated'
            os.remove('fppass.csv')
            os.remove('recentPlogin.csv')
            self.manager.current= 'Phome'
        else:
            widget.text= "Password doesn't match"

class AdvanceBooking(Screen):
    def on_text_pickup(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.choice= 'pickup'
        self.pickup_sug= []
        for i in suggestions[:3]:
            a= location(location= i[0], coords= i[1])
            self.pickup_sug.append(a)
        self.ids.suggest1.text= suggestions[0][0]
        self.ids.suggest2.text= suggestions[1][0]
        self.ids.suggest3.text= suggestions[2][0]

    def on_text_destination(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.destination_sug= []
        self.choice= "destination"
        for i in suggestions[:3]:
            a= location(location= i[0], coords= i[1])
            self.destination_sug.append(a)
        self.ids.suggest1.text= suggestions[0][0]
        self.ids.suggest2.text= suggestions[1][0]
        self.ids.suggest3.text= suggestions[2][0]

    def select_option(self, suggestion,pos,textWidget):
        try:
            textWidget.text = suggestion
            if self.choice== 'pickup':
                lon= self.pickup_sug[pos].coords[0]
                lat= self.pickup_sug[pos].coords[1]
                self.ids.pickup.text= self.pickup_sug[pos].location
                self.update_map_coordinates(lat, lon)                                                                                                                                                                                                                                                   
                self.update_marker(self.ids.pickupmarker, lat, lon)
            elif self.choice== 'destination':
                lon= self.destination_sug[pos].coords[0]
                lat= self.destination_sug[pos].coords[1]
                self.ids.drop.text= self.pickup_sug[pos].location
                self.update_map_coordinates(lat, lon)
                self.update_marker(self.ids.destinationmarker, lat, lon)
        except:
            textWidget.text= 'No text available'
    def update_map_coordinates(self, lat, lon):
        mapview = self.ids.passmap
        mapview.lat = lat
        mapview.lon = lon
    def update_marker(self, marker, lat, long):
        marker.lat= lat
        marker.lon= long
    def set_option(self, vehicle):
        self.ids.vehicle.text = vehicle
    def generate_price(self):
        pickupMarker = self.ids.pickupmarker
        destinationMarker = self.ids.destinationmarker
        lat1 = pickupMarker.lat
        lon1 = pickupMarker.lon
        lat2 = destinationMarker.lat
        lon2 = destinationMarker.lon
        vehicle_type = self.ids.vehicle.text
        myMap = map.API()
        distance = myMap.get_details(lat1, lon1, lat2, lon2)[1]
        date = self.ids.date.text
        time = self.ids.time.text
        price = priceGen.adv_price_gen(distance, vehicle_type, date, time)[-1]
        self.ids.price_text.text = str(price)
    def book_advanced(self):
        pickup = self.ids.pickup.text
        drop = self.ids.drop.text
        lat1 = self.ids.pickupmarker.lat
        lon1 = self.ids.pickupmarker.lon
        lat2 = self.ids.destinationmarker.lat
        lon2 = self.ids.destinationmarker.lon
        vehicle_type = self.ids.vehicle.text
        date = self.ids.date.text
        time = self.ids.time.text
        details = priceGen.book_advanced(lat1, lon1, lat2, lon2, vehicle_type, date, time)
        print(details)
        print(f"Pickup: {pickup}\nDrop: {drop}\nVehicle Type: {vehicle_type}\nPrice: {details["price"]}\nDriver Name: {details["driver_name"]}\nVehicle Number: {details["vehicle_number"]}\nOTP: {details["otp"]}\nBasic Fee: {details["basic"]}\nGST: {details["gst"]}\nConvenience Fee: {details["convenience"]}\nInsurance: {details["insurance"]}\nAdvance Booking Fee: {details["advance"]}\n Time of Arrival: {details["time_to_arrive"]}\nTravel Time: {details["time_of_travel"]}")
        # advanced_ride_details_screen = AdvancedRideDetailsScreen(pickup, drop, vehicle_type, details["price"], details["driver_name"], details["vehicle_number"], details["otp"], details["basic"], details["gst"], details["convenience"], details["insurance"], details["advance"])
        # self.manager.current = 'advancedridedetails'
        # self.manager.transition.direction = 'left'

class Profileviewer(Screen):
    def on_enter(self, *args):
        scroll= self.ids.ridelay
        f= open('recentPlogin.csv', 'r')
        reader= csv.reader(f)
        for i in reader:
            if len(i)>1:
                user= i[2]
        det= db.getUser(user)
        f.close()
        if det!= "error":
            self.ids.name.text= det['name']
            self.ids.email.text= det['email']
            self.ids.phone.text= det['phone']
        self.grid= GridLayout(cols= 5)
        self.l1= Label(text= 'Date', markup= True)
        self.l2= Label(text= 'Driver',markup= True)
        self.l3= Label(text= 'Pickup Location',markup= True)
        self.l4= Label(text= 'Destination',markup= True)
        self.l5= Label(text= 'Ride Fare',markup= True)
        self.grid.add_widget(self.l1)
        self.grid.add_widget(self.l2)
        self.grid.add_widget(self.l3)
        self.grid.add_widget(self.l4)
        self.grid.add_widget(self.l5)
        rides= db.getRidesOfUsers(userID= user)
        for j in range(len(rides)):
            i= rides[j]
            driv= db.getDriver(i['driverID'])
            pickup= db.get_address(i['start_lat'], i['start_long'])
            destination= db.get_address(i['end_lat'], i['end_long'])
            l1= Label(text= f"{i['date']}", size_hint= [0.2, 1])
            l2= Label(text= f"{driv['name']}",size_hint= [0.2, 1])
            l3= Label(text= f'{pickup}',size_hint= [0.2, 1])
            l4= Label(text= f'{destination}',size_hint= [0.2, 1])
            l5= Label(text= f"{i['price']}",size_hint= [0.2, 1])
            self.grid.add_widget(l1)
            self.grid.add_widget(l2)
            self.grid.add_widget(l3)
            self.grid.add_widget(l4)
            self.grid.add_widget(l5)
        scroll.add_widget(self.grid)

class PassengerHome(Screen):
    def on_text_pickup(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.pickup_sug= []
        self.choice= 'pickup'
        for i in suggestions[:3]:
            a= location(location= i[0], coords= i[1])
            self.pickup_sug.append(a)
        self.ids.suggest1.text= suggestions[0][0]
        self.ids.suggest2.text= suggestions[1][0]
        self.ids.suggest3.text= suggestions[2][0]
    def on_text_destination(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.destination_sug= []
        self.choice= "destination"
        for i in suggestions[:3]:
            a= location(location= i[0], coords= i[1])
            self.destination_sug.append(a)
        self.ids.suggest1.text= suggestions[0][0]
        self.ids.suggest2.text= suggestions[1][0]
        self.ids.suggest3.text= suggestions[2][0]
    def select_option(self, suggestion,pos ,textWidget):
        try:
            textWidget.text = suggestion
            if self.choice== 'pickup':
                lon= self.pickup_sug[pos].coords[0]
                lat= self.pickup_sug[pos].coords[1]
                self.ids.pickup.text= self.pickup_sug[pos].location
                self.update_map_coordinates(lat, lon)
                self.update_marker(self.ids.pickupmarker, lat, lon)
            elif self.choice== 'destination':
                lon= self.destination_sug[pos].coords[0]
                lat= self.destination_sug[pos].coords[1]
                self.ids.drop.text= self.pickup_sug[pos].location
                self.update_map_coordinates(lat, lon)
                self.update_marker(self.ids.destinationmarker, lat, lon)
        except:
            textWidget.text= 'No text available'
    def update_map_coordinates(self, lat, lon):
        mapview = self.ids.passmap
        mapview.lat = lat
        mapview.lon = lon
    def set_option(self, vehicle):
        self.ids.vehicle.text = vehicle
    def update_marker(self, marker, lat, lon):
        marker.lat= lat
        marker.lon= lon
    def generate_price(self):
        pickupMarker = self.ids.pickupmarker
        destinationMarker = self.ids.destinationmarker
        lat1 = pickupMarker.lat
        lon1 = pickupMarker.lon
        lat2 = destinationMarker.lat
        lon2 = destinationMarker.lon
        print(lat1, lon1, lat2, lon2)
        vehicle_type = self.ids.vehicle.text
        myMap = map.API()
        distance = myMap.get_details(lat1, lon1, lat2, lon2)[1]
        print(distance)
        price = priceGen.price_gen(distance, vehicle_type)
        print(price)
        self.ids.price_text.text = str(price[-1])
    def book_now(self):
        pickup = self.ids.pickup.text
        drop = self.ids.drop.text
        pickupMarker = self.ids.pickupmarker
        destinationMarker = self.ids.destinationmarker
        lat1 = pickupMarker.lat
        lon1 = pickupMarker.lon
        lat2 = destinationMarker.lat
        lon2 = destinationMarker.lon
        print(lat1, lon1, lat2, lon2)
        vehicle_type = self.ids.vehicle.text
        details = priceGen.book_now(lat1, lon1, lat2, lon2, vehicle_type)
        print(details)
        print(f"Pickup: {pickup}\nDrop: {drop}\nVehicle Type: {vehicle_type}\nPrice: {details["price"]}\nDriver Name: {details["driver_name"]}\nVehicle Number: {details["vehicle_number"]}\nOTP: {details["otp"]}\nBasic Fee: {details["basic"]}\nGST: {details["gst"]}\nConvenience Fee: {details["convenience"]}\nInsurance: {details["insurance"]}\n Time of Arrival: {details["time_to_arrive"]}\nTravel Time: {details["time_of_travel"]}")
        # ride_details_screen = RideDetailsScreen(pickup, drop, vehicle_type, details["price"], details["driver_name"], details["vehicle_number"], details["otp"], details["basic"], details["gst"], details["convenience"], details["insurance"])
        # self.manager.current = 'ridedetails'


class RideDetailsScreen(Screen):
    def __init__(self, pickup_text, drop_text, vehicle_type, price_generated, driver_name, vehicle_number, otp, basic, gst, convenience, insurance,**kwargs):
        super(RideDetailsScreen, self).__init__(**kwargs)
        self.pickup_location_text = pickup_text
        self.destination_location_text = drop_text
        self.vehicle_type = vehicle_type
        self.basic = basic
        self.gst = gst
        self.convenience = convenience
        self.insurance = insurance
        self.total_price = price_generated
        self.driver_name_text = driver_name
        self.vehicle_number = vehicle_number
        self.otp = otp
    def goBack(self):
        self.manager.current = 'Phome'


class AdvancedRideDetailsScreen(Screen):
    def __init__(self, pickup_text, drop_text, vehicle_type, price_generated, driver_name, vehicle_number, otp, basic, gst, convenience, insurance, advance_fee, **kwargs):
        super(AdvancedRideDetailsScreen, self).__init__(**kwargs)
        self.pickup_location_text = pickup_text
        self.destination_location_text = drop_text
        self.vehicle_type = vehicle_type
        self.basic = basic
        self.gst = gst
        self.convenience = convenience
        self.insurance = insurance
        self.advance_fee = advance_fee
        self.total_price = price_generated
        self.driver_name_text = driver_name
        self.vehicle_number = vehicle_number
        self.otp_text = otp
    def goBack(self):
        self.manager.current = 'Phome'

class location():
    def __init__(self, location, coords):
        self.location = location
        self.coords = coords


class Windows(ScreenManager):
    pass

kv= Builder.load_file("design.kv")

class CabBookingApp(App):
    def build(self):
        return kv
    
if __name__ == '__main__':
    CabBookingApp().run()