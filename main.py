from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import csv, os
import auth
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview.view import MapView, MapLayer
from kivy_garden.mapview.view import MapMarker
from kivy_garden.mapview import geojson
from kivy.graphics import Color, Line
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
        try:
            check= db.startUser(email=email, password=password)
            check_mail= db.forgotUser(email= email)
            if check != "error" and check['password']==password:
                self.otp= auth.gen_otp()
                
                response= auth.mail(email, check['name'], self.otp)
                f= open("recentPlogin.csv", 'w')
                writer= csv.writer(f)
                writer.writerow([email, password, check['userID']])
                self.user_id= check['userID']
                f.close()
                if response== "error":
                    widget.text= "Some Error occurred"
                else:
                    widget.text="OTP sent to your Mail"
            elif check=='error' and check_mail!='error':
                widget.text= 'Incorrect Password'
            else:
                widget.text= 'Email does not exist'
        except:
            widget.text= "No Internet Connected\n        Or\n   Server Not Active"

    def __verify__(self, otp, widget):  
        try:
            if self.otp==otp:
                widget.text= 'OTP Verified'
                self.manager.user_id= self.user_id
                self.manager.current ='Phome'
            else:
                widget.text= 'Incorrect OTP'
        except:
            widget.text= "Enter Valid Information"
            
class PassengerSP(Screen):
    def __enter_data__(self, name, phone, email,pwd ,cpwd, widget):  
        try:
            if pwd==cpwd:
                insert= db.postUser(name, email ,phone, pwd)
                if insert=='error':
                    widget.text= 'email or phone already exists'
                else:
                    self.otp= auth.gen_otp()
                    auth.mail(email, name, self.otp)
                    widget.text= "OTP Sent to your Email ID"
        except:
            widget.text= "No Internet Connection found"

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
    pick=0
    des=0
    def on_enter(self):
        plat= self.ids.pickupmarker.lat
        dlat= self.ids.destinationmarker.lat
        plon= self.ids.pickupmarker.lon
        dlon= self.ids.pickupmarker.lon
        self.route_map(plat, dlat, plon, dlon, self.ids.passmap)
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
                self.picklon= self.pickup_sug[pos].coords[0]
                self.picklat= self.pickup_sug[pos].coords[1]
                self.ids.pickup.text= self.pickup_sug[pos].location
                self.update_map_coordinates(self.picklat, self.picklon)                                                                                                                                                                                                                                                   
                self.update_marker(self.ids.pickupmarker, self.picklat, self.picklon)
                self.pick=1
            elif self.choice== 'destination':
                self.deslon= self.destination_sug[pos].coords[0]
                self.deslat= self.destination_sug[pos].coords[1]
                self.ids.drop.text= self.pickup_sug[pos].location
                self.update_map_coordinates(self.deslat, self.deslon)
                self.update_marker(self.ids.destinationmarker, self.deslat, self.deslon)
                self.des=1
            if self.pick and self.des:
                self.route_map(start_lat= self.picklat, end_lat= self.deslat, start_lon= self.picklon, end_lon= self.deslon, map= self.ids.passmap)
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

    def route_map(self, start_lat, end_lat, start_lon, end_lon, map):
        pass
        #route= db.route(start_lat, end_lat, start_lon, end_lon)
        #routeline= MapPolyLine(points= route, line_color= [0,1,0,1])
        #map.add_polyline(routeline)

        
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
        ride= db.postRide(self.manager.user_id, details['driverID'], lat1, lon1, lat2, lon2, True, details['price'])
        #pickup, drop, vehicle_type, details["price"], details["driver_name"], details["vehicle_number"], details["otp"], details["basic"], details["gst"], details["convenience"], details["insurance"], details["advance"]
        self.manager.advance_shared_data = AdvanceSharedData(
            pickup= pickup, 
            drop_text= drop, 
            vehicle= vehicle_type, 
            price= details["price"], 
            driver_name= details["driver_name"], 
            vehicle_no= details["vehicle_number"], 
            driver_phone = details["phone"],
            otp= details['otp'], 
            basic_pr= details['basic'], 
            gst=details["gst"], 
            convenience= details["convenience"], 
            insurance= details["insurance"], 
            advance= details["advance"],
            pick_marker= [lat1, lon1], 
            des_marker= [lat2, lon2], 
            date=date, 
            time= time,
            ride_id= ride["rideID"],
            ride_distance= details["ride_distance"],
            duration= details["duration"],
            time_of_travel= details["time_of_travel"]
            )
        self.manager.current = 'advancedridedetails'
        # self.manager.transition.direction = 'left'

class Profileviewer(Screen):
    def on_enter(self, *args):
        scroll = self.ids.ridelay
        scroll.clear_widgets()
        
        with open('recentPlogin.csv', 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if len(i) > 1:
                    user = i[2]
                    break
        
        det = db.getUser(user)
        
        if det != "error":
            self.ids.name.text = det['name']
            self.ids.email.text = det['email']
            self.ids.phone.text = det['phone']
        
        self.grid = GridLayout(cols=5, row_default_height='130dp', row_force_default=True, spacing=30, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.l1 = Label(text='Date', markup=True)
        self.l2 = Label(text='Driver', markup=True)
        self.l3 = Label(text='Pickup Location', markup=True)
        self.l4 = Label(text='Destination', markup=True)
        self.l5 = Label(text='Ride Fare', markup=True)
        
        self.grid.add_widget(self.l1)
        self.grid.add_widget(self.l2)
        self.grid.add_widget(self.l3)
        self.grid.add_widget(self.l4)
        self.grid.add_widget(self.l5)
        
        rides = db.getRidesOfUsers(userID=user)
        for i in rides:
            driv = db.getDriver(i['driverID'])
            pickup = db.get_address(i['start_lat'], i['start_long']).replace(",", "\n")
            destination = db.get_address(i['end_lat'], i['end_long']).replace(",", "\n")
            
            l1 = Label(text=f"{i['date']}", size_hint=[0.2, 1])
            l2 = Label(text=f"{driv['name']}", size_hint=[0.2, 1])
            l3 = Label(text=f'{pickup}', size_hint=[0.2, 1])
            l4 = Label(text=f'{destination}', size_hint=[0.2, 1])
            l5 = Label(text=f"{i['price']}", size_hint=[0.2, 1])
            
            self.grid.add_widget(l1)
            self.grid.add_widget(l2)
            self.grid.add_widget(l3)
            self.grid.add_widget(l4)
            self.grid.add_widget(l5)
        
        scroll.add_widget(self.grid)

class SharedRideData():
    def __init__(self, rideID=None, ):
        self.ride= rideID 

class PassengerHome(Screen):
    def on_enter(self):
        self.pick=0
        self.des= 0

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
                self.pick=1
            elif self.choice== 'destination':
                lon= self.destination_sug[pos].coords[0]
                lat= self.destination_sug[pos].coords[1]
                self.ids.drop.text= self.pickup_sug[pos].location
                self.update_map_coordinates(lat, lon)
                self.update_marker(self.ids.destinationmarker, lat, lon)
                self.des=1
            if self.pick and self.des:
                self.route_map(start_lat= self.picklat, end_lat= self.deslat, start_lon= self.picklon, end_lon= self.deslon, map= self.ids.passmap)
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
    
    def route_map(self, start_lat, end_lat, start_lon, end_lon, instance):
        route_layer= MapLayer()
        for layer in map.layers[:]:
            if isinstance(layer, MapLayer):
                map.remove_layer(layer)
        route= db.route(start_lat, end_lat, start_lon, end_lon)
        for point in route:
            route_layer.add_point(point[1], point[0])
        map.add_layer(route_layer)

    def generate_price(self):
        pickupMarker = self.ids.pickupmarker
        destinationMarker = self.ids.destinationmarker
        lat1 = pickupMarker.lat
        lon1 = pickupMarker.lon
        lat2 = destinationMarker.lat
        lon2 = destinationMarker.lon
        vehicle_type = self.ids.vehicle.text
        myMap = map.API()
        if lat1 and lon1 and lat2 and lon2:
            distance = myMap.get_details(lat1, lon1, lat2, lon2)[1]
            price = priceGen.price_gen(distance, vehicle_type)
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
        vehicle_type = self.ids.vehicle.text
        details = priceGen.book_now(lat1, lon1, lat2, lon2, vehicle_type)
        ride= db.postRide(self.manager.user_id, details['driverID'], lat1, lon1, lat2, lon2, False, details['price'])
        self.manager.shared_data= SharedData(
            pickup=pickup, 
            drop_text= drop, 
            vehicle=vehicle_type, 
            price=details["price"], 
            driver_name=details["driver_name"], 
            vehicle_no=details["vehicle_number"],
            driver_phone=details["phone"], 
            otp=details["otp"], 
            basic_pr=details["basic"], 
            gst= details["gst"], 
            convenience=details["convenience"], 
            insurance=details["insurance"], 
            ride_distance=details["ride_distance"],
            pick_marker= [lat1, lon2], 
            des_marker= [lat2, lon2], 
            duration=details["duration"], 
            time_of_travel=details["time_of_travel"], 
            ride_id=ride['rideID']
            )
        self.manager.current = 'ridedetails'


class SharedData():
    def __init__(self, pickup=None, drop_text=None, vehicle=None, price=None, driver_name=None, vehicle_no=None, driver_phone=None, otp=None, basic_pr=None, gst=None, convenience= None, insurance=None, pick_marker= None, des_marker= None, ride_distance=None, duration=None, time_of_travel = None, ride_id= None):
        self.pickup_location_text = pickup
        self.destination_location_text = drop_text
        self.vehicle_type = vehicle
        self.driver_phone = driver_phone
        self.basic = basic_pr
        self.gst = gst
        self.convenience = convenience
        self.insurance = insurance
        self.total_price = price
        self.driver_name_text = driver_name
        self.vehicle_number = vehicle_no
        self.otp_text = otp
        self.pick_marker= pick_marker
        self.des_marker= des_marker
        self.ride_distance = ride_distance
        self.duration = duration
        self.time_of_arrival = time_of_travel
        self.rideID= ride_id

class AdvanceSharedData():
    def __init__(self, pickup=None, drop_text=None, vehicle=None, price=None, driver_name=None, vehicle_no=None, driver_phone=None, otp=None, basic_pr=None, gst=None, convenience= None, insurance=None, advance=None, pick_marker= None, des_marker= None, time= None, date= None, ride_distance=None, duration = None, time_of_travel = None, ride_id = None):
        self.pickup_location_text = pickup
        self.destination_location_text = drop_text
        self.vehicle_type = vehicle
        self.driver_phone = driver_phone
        self.basic = basic_pr
        self.gst = gst
        self.convenience = convenience
        self.insurance = insurance
        self.advance = advance
        self.total_price = price
        self.driver_name_text = driver_name
        self.vehicle_number = vehicle_no
        self.otp_text = otp
        self.pick_marker= pick_marker
        self.des_marker= des_marker
        self.time= time
        self.date= date
        self.ride_distance = ride_distance
        self.duration = duration
        self.time_of_arrival = time_of_travel
        self.rideID = ride_id

class RideDetailsScreen(Screen):
    def on_enter(self):
        details = self.manager.shared_data
        self.pickup_location_text = details.pickup_location_text
        self.destination_location_text = details.destination_location_text
        self.vehicle_type = details.vehicle_type
        self.basic = details.basic
        self.gst = details.gst
        self.convenience = details.convenience
        self.insurance = details.insurance
        self.total_price = details.total_price
        self.driver_name_text = details.driver_name_text
        self.vehicle_number = details.vehicle_number
        self.otp = details.otp_text
        # New
        self.driver_phone = details.driver_phone
        self.ride_distance = details.ride_distance
        self.duration = details.duration
        self.time_of_arrival = details.time_of_arrival

        self.ids.dname.text= self.driver_name_text
        self.ids.dvehicletype.text= (self.vehicle_type).upper()
        self.ids.dvehicleno.text= self.vehicle_number
        self.ids.otp.text= 'OTP: '+str(self.otp)
        self.ids.pickup.text= 'Pickup: '+self.pickup_location_text
        self.ids.destination.text= 'Drop: '+ self.destination_location_text
        self.ids.price.text= 'Price: '+ str(self.total_price)
        self.ids.basic.text= 'Basic price: '+ str(self.basic)
        self.ids.gst.text= 'GST: '+str(self.gst)
        self.ids.convenience.text= 'Convenience Fee: '+str(self.convenience)
        self.ids.insurance.text= 'Insurance: '+str(self.insurance)
        # New
        self.ids.driver_phone.text = 'Phone: ' + str(self.driver_phone)
        self.ids.ride_distance.text='Ride Distance: ' + str(self.ride_distance) + " km"
        self.ids.duration.text = 'Travel Time: '+ str(self.duration) + " mins"
        self.ids.time_of_arrival.text = "Driver is " + str(self.time_of_arrival) + " minutes away"

    def goBack(self):
        self.manager.current = 'Phome'

    def cancel_ride(self):
        pass
        

class AdvancedRideDetailsScreen(Screen):
    def on_enter(self):
        details = self.manager.advance_shared_data
        self.pickup_location_text = details.pickup_location_text
        self.destination_location_text = details.destination_location_text
        self.vehicle_type = details.vehicle_type
        self.driver_phone = details.driver_phone
        self.basic = details.basic
        self.gst = details.gst
        self.convenience = details.convenience
        self.insurance = details.insurance
        self.total_price = details.total_price
        self.driver_name_text = details.driver_name_text
        self.vehicle_number = details.vehicle_number
        self.otp = details.otp_text
        # New
        self.date = details.date
        self.time = details.time
        self.advance = details.advance
        self.ride_distance = details.ride_distance
        self.duration = details.duration
        self.time_of_arrival = details.time_of_arrival

        self.ids.dname.text= self.driver_name_text
        self.ids.dvehicletype.text= (self.vehicle_type).upper()
        self.ids.dvehicleno.text= self.vehicle_number
        self.ids.otp.text= 'OTP: '+str(self.otp)
        self.ids.pickup.text= 'Pickup: '+self.pickup_location_text
        self.ids.destination.text= 'Drop: '+ self.destination_location_text
        self.ids.price.text= 'Price: '+ str(self.total_price)
        self.ids.basic.text= 'Basic price: '+ str(self.basic)
        self.ids.gst.text= "GST: "+str(self.gst)
        self.ids.convenience.text= "Convenience Fee: "+str(self.convenience)
        self.ids.insurance.text= "Insurance: "+str(self.insurance)
        # New
        self.ids.date.text = "Date: " + str(self.date)
        self.ids.time.text = "Time: " + str(self.time)
        self.ids.driver_phone.text = "Phone: " + str(self.driver_phone)
        self.ids.advance.text = "Advance: " + str(self.advance)
        self.ids.ride_distance.text = 'Ride Distance: '+str(self.ride_distance) + " km"
        self.ids.duration.text = 'Travel Time: '+ str(self.duration) + " mins"
        self.ids.time_of_arrival.text = "Driver is " + str(self.time_of_arrival) + " minutes away"

    def goBack(self):
        self.manager.current = 'Phome'

    def cancel_ride(self):
        pass

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
