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
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.spinner import Spinner
import socketio
import threading

# Initialize Socket.IO client
sio = socketio.Client()

class Chatscreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', padding= [30], spacing= 10)
        with self.layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.message_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.message_list.bind(minimum_height=self.message_list.setter('height'))
        self.scroll_view.add_widget(self.message_list)

        self.input_box = BoxLayout(size_hint=(1, 0.1))
        self.text_input = TextInput(size_hint=(0.8, 1), hint_text= "type here")
        self.send_button = Button(text='Send', font_size= 20,size_hint=(0.2, 1), color= [0.8,0.8,0.8,1], background_color= [0.8, 0.2, 0.2, 1])
        self.send_button.bind(on_press=self.send_message)
        self.back_button= Button(text= 'back',font_size= 20 ,size_hint=(0.1, 1), color= [0.8,0.8,0.8,1], background_color= [0.8, 0.2, 0.2, 1])
        self.back_button.bind(on_press=self.go_back)
        self.input_box.add_widget(self.text_input)
        self.input_box.add_widget(self.send_button)
        self.input_box.add_widget(self.back_button)
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.input_box)

        threading.Thread(target=self.connect_to_server, daemon=True).start()
        sio.on('message', self.receive_message)
        self.add_widget(self.layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_back(self, instance):
        sio.disconnect()
        self.manager.current= 'Phome'
    
    def connect_to_server(self):
        try:
            sio.connect('http://127.0.0.1:6000/')  # Use your actual server URL
            sio.on('connect', self.on_connect)
            sio.on('disconnect', self.on_disconnect)
        except Exception as e:
            print(f"Connection error: {e}")

    def on_connect(self):
        print("Connected to server")
        self.is_connected = True

    def on_disconnect(self):
        print("Disconnected from server")
        self.is_connected = False

    def send_message(self, instance):
        message = self.manager.user_name+": "+self.text_input.text
        self.sent_msg = message
        if message:
            sio.send(message)
            self.text_input.text = ''
        boxlay= BoxLayout(orientation='horizontal', size_hint_y=None,height=40)
        label = Label(text=f"{message}",font_size= 20, size_hint_x=0.5,size_hint_y=None, height=40, halign='right', valign='center', color= [0,0,0,1])
        label2= Label(text='',size_hint_x=0.5,size_hint_y=None, height=40)
        boxlay.add_widget(label2)
        boxlay.add_widget(label)
        
        self.message_list.add_widget(boxlay)
        self.scroll_view.scroll_to(label)

    def receive_message(self, msg):
        if self.sent_msg:
            if self.sent_msg == msg:
                self.sent_msg = ''
                return
        self.add_message_to_ui(msg, "received")

    @mainthread
    def add_message_to_ui(self, msg, msg_type):
        if msg_type == "received":
            boxlay= BoxLayout(orientation='horizontal', size_hint_y=None,height=40)
            label = Label(text=msg,font_size= 20,size_hint_x= 0.5, size_hint_y=None, height=40, halign='left', valign='center', color= [0,0,0,1])
            label2 = Label(text='',size_hint_x= 0.5, size_hint_y=None, height=40, halign='left', valign='center')
            boxlay.add_widget(label)
            boxlay.add_widget(label2)
        self.message_list.add_widget(boxlay)
        self.scroll_view.scroll_to(label)


class DriverChat(Screen):
    def on_enter(self):
        self.msg_sent = 0
        self.username = self.manager.user_name
        self.room = self.manager.user_name
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=[20])
        with self.root.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=self.root.size, pos=self.root.pos)
            self.root.bind(size=self._update_rect, pos=self._update_rect)
            
        self.scroll_view = ScrollView()
        self.message_layout = GridLayout(cols=2, size_hint_y=None)
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))
        self.scroll_view.add_widget(self.message_layout)

        self.root.add_widget(self.scroll_view)
        
        self.input_layout = BoxLayout(size_hint_y=None, height='40dp')
        self.msg_input = TextInput(hint_text='Message', size_hint_y=None, height='40dp')
        self.send_button = Button(text='Send', size_hint=(0.1, 1), height='40dp', on_press=self.send_message, font_size=20, color=[0.8,0.8,0.8,1], background_color=[0.8, 0.2, 0.2, 1])
        self.back_button = Button(text='Back', size_hint=(0.1, 1), height='40dp', on_press=self.go_back, font_size=20, color=[0.8,0.8,0.8,1], background_color=[0.8, 0.2, 0.2, 1])
        self.input_layout.add_widget(self.msg_input)
        self.input_layout.add_widget(self.send_button)
        self.input_layout.add_widget(self.back_button)
        self.root.add_widget(self.input_layout)

        self.msg_text = self.msg_input.text

        threading.Thread(target=self.connect_to_server, daemon=True).start()
        sio.on('message', self.receive_message)
        self.add_widget(self.root)
    
    def connect_to_server(self):
        try:
            sio.connect('http://127.0.0.1:5000/')  # Use your actual server URL
            sio.on('connect', self.on_connect)
            sio.on('disconnect', self.on_disconnect)
            sio.emit('join', {'username': self.username, 'room': self.room})
        except Exception as e:
            print(f"Connection error: {e}")
    
    def on_connect(self):
        print("Connected to server")
        self.is_connected = True

    def on_disconnect(self):
        print("Disconnected from server")
        self.is_connected = False


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def leave_room(self):
        sio.disconnect()
    
    def go_back(self, instance):
        self.leave_room()
        self.manager.current = 'ridedetails'
    
    def send_message(self, instance):
        self.msg_text = self.msg_input.text
        self.msg_input.text = ''
        msg_label2 = Label(text='', size_hint_y=None, height='40dp')
        msg_label = Label(text=f"{self.username}: {self.msg_text}", size_hint_y=None, height='40dp', color=[0, 0, 0, 1])
        self.message_layout.add_widget(msg_label2)
        self.message_layout.add_widget(msg_label)
        self.scroll_view.scroll_to(msg_label)
        sio.emit('message', {'room': self.room, 'msg': f"{self.username}: {self.msg_text}"})

    def receive_message(self, data):
        print(f"Received message: {data}")
        Clock.schedule_once(lambda dt: self.display_message(data))

    def display_message(self, message):
        if message != f"{self.username}: {self.msg_text}":
            msg_label = Label(text=message, size_hint_y=None, height='40dp', color=[0, 0, 0, 1])
            msg_label2 = Label(text='', size_hint_y=None, height='40dp')
            self.message_layout.add_widget(msg_label)
            self.message_layout.add_widget(msg_label2)
            self.scroll_view.scroll_to(msg_label)
        self.msg_text= ''

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
            print(check)
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
                    self.manager.user_name= check["name"]
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
            self.manager.current= 'Phome'
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

class ViewRides(Screen):
    def on_enter(self):
        self.ids.options_lay.clear_widgets()
        ride= self.manager.ride_data
        self.ride_id= ride.ride
        self.ids.dname.text= ride.dname
        self.ids.dvehicletype.text= ride.vehicle_type
        self.ids.dvehicleno.text= ride.vehicle_no
        self.ids.driver_phone.text= ride.driver_phone
        self.ids.otp.text= f"[b]OTP:[/b] [color=ff0000]{str(self.gen_otp())}[/color]"
        ride.pick_loc= ride.pick_loc.replace("\n", ",")
        ride.des_loc= ride.des_loc.replace("\n", ",")
        self.ids.pickup.text= "Pickup: "+ ride.pick_loc
        self.ids.destination.text= "Destination: "+ride.des_loc
        self.ids.price.text= "Price: "+ str(ride.ride_price)
        self.ids.pickupmarker.lat= ride.pick_coords[0]
        self.ids.pickupmarker.lon= ride.pick_coords[1]
        self.ids.destinationmarker.lat= ride.des_coords[0]
        self.ids.destinationmarker.lon= ride.des_coords[1]
        self.map = self.ids.passmap
        self.map.update_lines(ride.route)
        self.rating= None

        if ride.ride_status=="ONGOING":
            options_lay= self.ids.options_lay
            options_lay.spacing= 10
            options_lay.size_hint= (1, 0.2)
            buttons_lay= BoxLayout(orientation= 'horizontal',
                                   padding= 5)
            buttons_lay.size_hint= [1, 0.5]
            buttons_lay.spacing= 5
            cancelbtn= Button(text= 'Cancel Ride', background_color= (1, 0.2, 0.2, 1), color= (1, 1, 1, 1))
            endbtn= Button(text= 'End Ride', background_color= (1, 0.2, 0.2, 1), color= (1, 1, 1, 1))
            #self.rating= TextInput(hint_text="Rating(1-5)", size_hint= [1, 0.1], multiline= False)

            self.spinner= Spinner(
                text= 'Rating',
                values= ('1', '2', '3', '4', '5'),
                size_hint= (1, 0.5),
                color= (0.8,0.8,0.8, 1),
                background_color= (0.8, 0.2,0.2, 1)
            )
            l1= Label(
                text= '',
            )
            self.spinner.bind(on_text= lambda instance: self.select_rating(self.spinner, self.spinner.text))
            cancelbtn.bind(on_press=self.cancel_call_back())
            endbtn.bind(on_release= self.end_call_back())
            options_lay.add_widget(self.spinner)
            buttons_lay.add_widget(cancelbtn)
            buttons_lay.add_widget(endbtn)
            options_lay.add_widget(buttons_lay)
            options_lay.add_widget(l1)
    
    def gen_otp(self):
        import random
        otp= ''
        val= '1234567890'
        nums= list(val)
        for i in range(4):
            otp += random.choice(nums)
        return otp
    
    def select_rating(self, spinner, text):
        if text.isdigit():
            self.rating= int(text)
        else:
            self.ids.errormsg.text= 'select the rating'


    def cancel_call_back(self):
        def callback(instance):
            cancellationFee = priceGen.cancelRide(rideID=self.ride_id)
            self.manager.get_screen('cancelscreen').update_result(cancellationFee)
            self.manager.current = 'cancelscreen'
        return callback
    
    def end_call_back(self):    
        def callback(instance):
            try:
                rating=int(self.spinner.text)
                rating= float(rating)
                db.completeRide(self.ride_id)
                ride= db.getRide(self.ride_id)
                db.giveRatings(ride["driverID"], rating)
                self._reset_()
                self.manager.current= 'Phome'
            except:
                self.ids.errormsg.text= 'Select Rating'
        return callback
    def _reset_(self):
        self.manager.ride_data= None

class AdvanceBooking(Screen):
    pick=0
    des=0
    def on_enter(self):
        self.map= self.ids.passmap
        try:
            plat= self.manager.pickup_lat
            dlat= self.manager.destination_lat
            plon= self.manager.pickup_lon
            dlon= self.manager.destination_lon
            self.ids.pickupmarker.lat= plat
            self.ids.pickupmarker.lon= plon
            self.ids.destinationmarker.lat= dlat
            self.ids.destinationmarker.lon= dlon
            self.ids.drop.text= self.manager.destination_text
            self.ids.pickup.text= self.manager.pickup_text
            self.route_map(plat, dlat, plon, dlon, self.ids.passmap)
        except:
            pass
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
                self.manager.pickup_lon = self.pickup_sug[pos].coords[0]
                self.picklat= self.pickup_sug[pos].coords[1]
                self.manager.pickup_lat = self.pickup_sug[pos].coords[1]
                self.ids.pickup.text= self.pickup_sug[pos].location
                self.update_map_coordinates(self.picklat, self.picklon)                                                                                                                                                                                                                                                   
                self.update_marker(self.ids.pickupmarker, self.picklat, self.picklon)
                self.pick=1
                try:
                    self.route_map(start_lat= self.picklat, end_lat= self.deslat, start_lon= self.picklon, end_lon= self.deslon, map= self.ids.passmap)
                except:
                    pass
            elif self.choice== 'destination':
                self.deslon= self.destination_sug[pos].coords[0]
                self.manager.destination_lon = self.destination_sug[pos].coords[0]
                self.deslat= self.destination_sug[pos].coords[1]
                self.manager.destination_lat = self.destination_sug[pos].coords[1]
                self.ids.drop.text= self.destination_sug[pos].location
                self.update_map_coordinates(self.deslat, self.deslon)
                self.update_marker(self.ids.destinationmarker, self.deslat, self.deslon)
                self.des=1
                try:
                    self.route_map(start_lat= self.picklat, end_lat= self.deslat, start_lon= self.picklon, end_lon= self.deslon, map= self.ids.passmap)
                except:
                    pass
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
        route= db.route(start_lat, end_lat, start_lon, end_lon)
        self.route= route
        map.update_lines(route)       
        
    def generate_price(self):
        try:
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
            self.ids.price_text.text = "Cost: Rs. "+str(price)
        except:
            self.ids.price_text.text= 'Fill all the fields to\n Check Price'
    def book_advanced(self):
        try:
            pickup = self.ids.pickup.text
            drop = self.ids.drop.text
            lat1 = self.ids.pickupmarker.lat
            lon1 = self.ids.pickupmarker.lon
            lat2 = self.ids.destinationmarker.lat
            lon2 = self.ids.destinationmarker.lon
            vehicle_type = self.ids.vehicle.text
            self.manager.pick_loc=[lat1, lon1]
            self.manager.des_loc=[lat2, lon2]
            date = self.ids.date.text
            time = self.ids.time.text
            dist= db.distance_time(lat1, lat2, lon1, lon2)
            if dist['distance']>400:
                self.ids.price_text.text = 'Cannot book as travel distance \nis more than 400kms'
                return 
            self.manager.route= self.route
            details = priceGen.book_advanced(lat1, lon1, lat2, lon2, vehicle_type, date, time)
            ride= db.postRide(self.manager.user_id, details['driverID'], lat1, lon1, lat2, lon2, True, details['price'], "ONGOING")
            self.manager.advance_shared_data = AdvanceSharedData(
                pickup= pickup, 
                drop_text= drop, 
                vehicle= vehicle_type, 
                price= details["price"], 
                driver_name= details["driver_name"], 
                vehicle_no= details["vehicle_number"], 
                driver_phone = details["phone"],
                otp= details['otp'], 
                basefee = details["basefee"],
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
        except:
            self.ids.price_text.text = 'enter all fields correctly'

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
        
        self.grid = GridLayout(cols=6, row_default_height='130dp', row_force_default=True, spacing=30, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.l1 = Label(text='Date', markup=True, color=[0, 0, 0, 1])
        self.l2 = Label(text='Driver', markup=True, color=[0, 0, 0, 1])
        self.l3 = Label(text='Pickup Location', markup=True, color=[0, 0, 0, 1])
        self.l4 = Label(text='Destination', markup=True, color=[0, 0, 0, 1])
        self.l5 = Label(text='Ride Fare', markup=True, color=[0, 0, 0, 1])
        self.l6 = Label(text= 'View Ride', markup= True,color= [0, 0, 0, 1])
        self.grid.add_widget(self.l1)
        self.grid.add_widget(self.l2)
        self.grid.add_widget(self.l3)
        self.grid.add_widget(self.l4)
        self.grid.add_widget(self.l5)
        self.grid.add_widget(self.l6)
        rides = db.getRidesOfUsers(userID=user)
        cnt=0
        buttons= []
        for j in range(len(rides)):
            i= rides[j]
            driv = db.getDriver(i['driverID'])
            pickup = db.get_address(i['start_lat'], i['start_long']).replace(",", "\n")
            destination = db.get_address(i['end_lat'], i['end_long']).replace(",", "\n")
            
            l1 = Label(text=f"{i['date']}", size_hint=[0.2, 1], color=[0, 0, 0, 1])
            l2 = Label(text=f"{driv['name']}", size_hint=[0.2, 1], color=[0, 0, 0, 1])
            l3 = Label(text=f'{pickup}', size_hint=[0.2, 1], color=[0, 0, 0, 1])
            l4 = Label(text=f'{destination}', size_hint=[0.2, 1], color=[0, 0, 0, 1])
            l5 = Label(text=f"{i['price']}", size_hint=[0.2, 1], color=[0, 0, 0, 1])
            b1 = Button(text= f"{i['rideID']}",
                        size_hint=[0.2, 0.5], 
                        color= [1, 1, 1, 1], 
                        background_color= [0.8, 0.2, 0.2, 1],
                        )
            buttons.append(b1)
            b1.bind(on_press=self.create_view_ride_callback(b1.text))
            cnt+=1
            self.grid.add_widget(l1)
            self.grid.add_widget(l2)
            self.grid.add_widget(l3)
            self.grid.add_widget(l4)
            self.grid.add_widget(l5)
            self.grid.add_widget(b1)
        scroll.add_widget(self.grid)      

    def create_view_ride_callback(self, ride_id):
        def callback(instance):
            self.view_ride(int(ride_id))
        return callback
    
    def view_ride(self, ride_id):
        # i["rideID"], pickup, destination, [[i['start_lat'], i['start_long']], [i['end_lat'], i['end_long']]]
        ride= db.getRide(ride_id)
        driver= db.getDriver(ride['driverID'])
        pickup_loc = db.get_address(ride['start_lat'], ride['start_long']).replace(",", "\n")
        des_loc = db.get_address(ride['end_lat'], ride['end_long']).replace(",", "\n")
        dname= driver['name']
        vtype= driver['vehicle_type']
        vno= driver['vehicle_number']
        dphone= driver['phone']
        ride_status= ride['status']
        pick_coords= [ride['start_lat'], ride['start_long']]
        des_coords= [ride['end_lat'], ride['end_long']]
        time_dist= db.distance_time(start_lat=ride['start_lat'], end_lat=ride['end_lat'], start_lon=ride['start_long'], end_lon=ride['end_long'])
        route= db.route(start_lat=ride['start_lat'], end_lat=ride['end_lat'], start_lon=ride['start_long'], end_lon=ride['end_long'])
        self.manager.ride_data= None
        self.manager.ride_data= RideData(rideID= ride['rideID'], 
                                        pickup= pickup_loc, 
                                        destination= des_loc, 
                                        pick_coords= pick_coords, 
                                        des_coords=des_coords, 
                                        price= ride['price'], 
                                        vehicle_no= vno, 
                                        vehicle_type= vtype,
                                        driver_name= dname,
                                        ride_status= ride['status'],
                                        driver_phone= dphone,
                                        route= route)
        self.manager.current= 'viewrides'



class RideData(object):
    def __init__(self, rideID=None, pickup=None, destination=None, pick_coords=None, des_coords=None, price=None, driver_name= None, driver_phone= None, vehicle_no= None, vehicle_type= None, ride_status= None, distance= None, time= None, route= None):
        self.ride= rideID
        self.pick_loc= pickup
        self.des_loc= destination
        self.pick_coords= pick_coords
        self.des_coords= des_coords
        self.ride_price= price
        self.dname= driver_name
        self.vehicle_no= vehicle_no
        self.vehicle_type= vehicle_type
        self.ride_status= ride_status
        self.driver_phone= driver_phone
        self.distance= distance
        self.ride_time= time
        self.route= route
         

class CustomMapView(MapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []  # To store the Line objects
        self.coordinates = []
    def update_lines(self, coordinates):
        # Store the coordinates for later use
        self.coordinates = coordinates
        self.redraw_lines()

    def redraw_lines(self, *args):
        # Clear previous lines from the canvas
        
        for line in self.lines:
            self.canvas.remove(line)
        self.lines.clear()

        if not self.coordinates:
            return

        # Draw new lines
        with self.canvas:
            Color(1, 0, 0, 1)  # Set the line color to red
            for i in range(len(self.coordinates) - 1):
                if self.valid_coordinates(self.coordinates[i]) and self.valid_coordinates(self.coordinates[i + 1]):
                    x1, y1 = self.convert_to_screen_coordinates(self.coordinates[i][1], self.coordinates[i][0])
                    x2, y2 = self.convert_to_screen_coordinates(self.coordinates[i + 1][1], self.coordinates[i+1][0])
                    # Draw the line between two points
                    line = Line(points=[x1, y1, x2, y2], width=2)
                    self.lines.append(line)

    def valid_coordinates(self, coord):
        # Check if the coordinates are valid (not None)
        return coord[0] is not None and coord[1] is not None

    def convert_to_screen_coordinates(self, lati, long):
        # Convert lat/lon to screen coordinates
        #lat, lon = lati, long
        return self.to_local(*super().get_window_xy_from(lati, long, self.zoom))


class PassengerHome(Screen):
    def on_enter(self):
        self.pick=0
        self.des= 0
        self.route_map(self.ids.pickupmarker.lat, self.ids.destinationmarker.lat,  self.ids.pickupmarker.lon,self.ids.destinationmarker.lon, self.ids.passmap)
        
    def on_text_pickup(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.pickup_sug= []
        self.choice= 'pickup'
        try:
            for i in suggestions[:3]:
                a= location(location= i[0], coords= i[1])
                self.pickup_sug.append(a)
            self.ids.suggest1.text= suggestions[0][0]
            self.ids.suggest2.text= suggestions[1][0]
            self.ids.suggest3.text= suggestions[2][0]
        except:
            self.ids.notify.text= "No Results available"

    def on_text_destination(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.destination_sug= []
        self.choice= "destination"
        try:
            for i in suggestions[:3]:
                a= location(location= i[0], coords= i[1])
                self.destination_sug.append(a)
            self.ids.suggest1.text= suggestions[0][0]
            self.ids.suggest2.text= suggestions[1][0]
            self.ids.suggest3.text= suggestions[2][0]
        except:
            self.ids.notify.text= "No Results available"
    def select_option(self, suggestion,pos ,textWidget):
        try:
            textWidget.text = suggestion
            if self.choice== 'pickup':
                lon= self.pickup_sug[pos].coords[0]
                lat= self.pickup_sug[pos].coords[1]
                self.manager.pickup_lat= lat
                self.manager.pickup_lon= lon
                
                self.ids.pickup.text= self.pickup_sug[pos].location
                self.manager.pickup_text= self.ids.pickup.text
                self.update_map_coordinates(lat, lon)
                self.update_marker(self.ids.pickupmarker, lat, lon)
                self.pick=1
                try:
                    self.route_map(start_lat= self.manager.pickup_lat, end_lat= self.manager.destination_lat, start_lon= self.manager.pickup_lon, end_lon= self.manager.destination_lon, map= self.ids.passmap)
                except:
                    pass
            elif self.choice== 'destination':
                lon= self.destination_sug[pos].coords[0]
                lat= self.destination_sug[pos].coords[1]
                self.ids.drop.text= self.destination_sug[pos].location
                self.manager.destination_text= self.ids.drop.text
                self.update_map_coordinates(lat, lon)
                self.update_marker(self.ids.destinationmarker, lat, lon)
                self.manager.destination_lat= lat
                self.manager.destination_lon= lon
                self.des=1
                try:
                    self.route_map(start_lat= self.manager.pickup_lat, end_lat= self.manager.destination_lat, start_lon= self.manager.pickup_lon, end_lon= self.manager.destination_lon, map= self.ids.passmap)
                except:
                    pass
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
    
    def route_map(self, start_lat, end_lat, start_lon, end_lon, map):
        route= db.route(start_lat, end_lat, start_lon, end_lon)
        self.route= route
        map.update_lines(route)

    def generate_price(self):
        try:
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
        except:
            self.ids.price.text='Enter the Pickup location\n and Destination'

    def book_now(self):
        try:
            pickup = self.ids.pickup.text
            drop = self.ids.drop.text
            pickupMarker = self.ids.pickupmarker
            destinationMarker = self.ids.destinationmarker
            lat1 = pickupMarker.lat
            lon1 = pickupMarker.lon
            lat2 = destinationMarker.lat
            lon2 = destinationMarker.lon
            vehicle_type = self.ids.vehicle.text
            dist= db.distance_time(lat1, lat2, lon1, lon2)
            if dist['distance']>100:
                self.ids.price_text.text= 'Cannot book as Travel distance\n is more than 100kms'
                return
            self.manager.pickup_loc= [lat1, lon1]
            self.manager.des_loc= [lat2, lon2]
            self.manager.route= self.route
            details = priceGen.book_now(lat1, lon1, lat2, lon2, vehicle_type)
            ride= db.postRide(self.manager.user_id, details['driverID'], lat1, lon1, lat2, lon2, False, details['price'], "ONGOING")
            self.manager.shared_data= SharedData(
                pickup=pickup, 
                drop_text= drop, 
                vehicle=vehicle_type, 
                price=details["price"], 
                driver_name=details["driver_name"], 
                vehicle_no=details["vehicle_number"],
                driver_phone=details["phone"], 
                otp=details["otp"], 
                basefee = details["basefee"],
                basic_pr=details["basic"], 
                gst= details["gst"], 
                convenience=details["convenience"], 
                insurance=details["insurance"], 
                ride_distance=details["ride_distance"],
                pick_marker= [lat1, lon2], 
                des_marker= [lat2, lon2], 
                driver_marker= details["driverCoord"],
                duration=details["duration"], 
                time_of_travel=details["time_of_travel"], 
                ride_id=ride['rideID']
            )
            self.manager.current = 'ridedetails'
        except:
            self.ids.price_text.text= 'Enter all fields correctly'


class SharedData():
    def __init__(self, pickup=None, drop_text=None, vehicle=None, price=None, driver_name=None, vehicle_no=None, driver_phone=None, otp=None, basic_pr=None, gst=None, convenience= None, insurance=None, pick_marker= None, des_marker= None, ride_distance=None, duration=None, time_of_travel = None, ride_id= None, driver_marker= None, basefee=None):
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
        self.driver_marker= driver_marker
        self.basefee = basefee
class AdvanceSharedData():
    def __init__(self, pickup=None, drop_text=None, vehicle=None, price=None, driver_name=None, vehicle_no=None, driver_phone=None, otp=None, basic_pr=None, gst=None, convenience= None, insurance=None, advance=None, pick_marker= None, des_marker= None, time= None, date= None, ride_distance=None, duration = None, time_of_travel = None, ride_id = None, basefee = None):
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
        self.basefee = basefee

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
        self.rideID = details.rideID
        # New
        self.basefee = details.basefee
        self.driver_phone = details.driver_phone
        self.ride_distance = details.ride_distance
        self.duration = details.duration
        self.time_of_arrival = details.time_of_arrival
        self.ids.pickupmarker.lat= self.manager.pickup_loc[0]
        self.ids.pickupmarker.lon= self.manager.pickup_loc[1]
        self.ids.destinationmarker.lat= self.manager.des_loc[0]
        self.ids.destinationmarker.lon= self.manager.des_loc[1]
        self.ids.driver_loc.lat= details.driver_marker[0]
        self.ids.driver_loc.lon= details.driver_marker[1]
        self.ids.dname.text= self.driver_name_text
        self.ids.dvehicletype.text= (self.vehicle_type).upper()
        self.ids.dvehicleno.text= self.vehicle_number
        self.ids.otp.text= f"[b]OTP:[/b] [color=ff0000]{str(self.otp)}[/color]"
        self.ids.pickup.text= 'Pickup: '+self.pickup_location_text
        self.ids.destination.text= 'Drop: '+ self.destination_location_text
        self.ids.price.text= 'Price: '+ str(self.total_price)
        self.ids.basic.text= 'Basic price: '+ str(self.basic)
        self.ids.gst.text= 'GST: '+str(self.gst)
        self.ids.convenience.text= 'Convenience Fee: '+str(self.convenience)
        self.ids.insurance.text= 'Insurance: '+str(self.insurance)
        # New
        self.ids.basefee.text = 'Vehicle Base Fee: ' + str(self.basefee)
        self.ids.driver_phone.text = 'Phone: ' + str(self.driver_phone)
        self.ids.ride_distance.text='Ride Distance: ' + str(self.ride_distance) + " km"
        self.ids.duration.text = 'Travel Time: '+ str(self.duration) + " mins"
        self.ids.time_of_arrival.text = f"Driver is [color=0000ff]{str(self.time_of_arrival)}[/color] minutes away"
        self.mapp= self.ids.bookmap
        self.mapp.update_lines(self.manager.route)

    def goBack(self):
        self.manager.current = 'Phome'

    def cancel_ride(self):
        cancellationFee = priceGen.cancelRide(rideID=self.rideID)
        self.manager.get_screen('cancelscreen').update_result(cancellationFee)
        self.manager.current = 'cancelscreen'

    def end_ride(self, rating):
        try:
            rating= float(rating)
            db.completeRide(self.rideID)
            ride= db.getRide(self.rideID)
            db.giveRatings(ride["driverID"], rating)
            print(ride)
            self.manager.current= 'Phome'
        except:
            self.ids.errormsg.text= "Give Rating in Integer or decimal"

class CancellationScreen(Screen):
    def update_result(self, computed_value):
        self.ids.cancelfee.text = "Cancellation Fee: " + str(computed_value)
    def goBack(self):
        self.manager.current = 'Phome'

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
        self.rideID = details.rideID
        # New
        self.basefee = details.basefee
        self.date = details.date
        self.time = details.time
        self.advance = details.advance
        self.ride_distance = details.ride_distance
        self.duration = details.duration
        self.time_of_arrival = details.time_of_arrival
        self.ids.pickupmarker.lat= self.manager.pick_loc[0]
        self.ids.pickupmarker.lon= self.manager.pick_loc[1]
        self.ids.destinationmarker.lat= self.manager.des_loc[0]
        self.ids.destinationmarker.lon= self.manager.des_loc[1]
        self.mapp= self.ids.bookmap
        self.mapp.update_lines(self.manager.route)

        self.ids.dname.text= self.driver_name_text
        self.ids.dvehicletype.text= (self.vehicle_type).upper()
        self.ids.dvehicleno.text= self.vehicle_number
        self.ids.otp.text= f"[b]OTP:[/b] [color=ff0000]{str(self.otp)}[/color]"
        self.ids.pickup.text= 'Pickup: '+self.pickup_location_text
        self.ids.destination.text= 'Drop: '+ self.destination_location_text
        self.ids.price.text= 'Price: '+ str(self.total_price)
        self.ids.basic.text= 'Basic price: '+ str(self.basic)
        self.ids.gst.text= "GST: "+str(self.gst)
        self.ids.convenience.text= "Convenience Fee: "+str(self.convenience)
        self.ids.insurance.text= "Insurance: "+str(self.insurance)
        # New
        self.ids.basefee.text = 'Vehicle Base Fee: ' + str(self.basefee)
        self.ids.date.text = "Date: " + str(self.date)
        self.ids.time.text = "Time: " + str(self.time)
        self.ids.driver_phone.text = "Phone: " + str(self.driver_phone)
        self.ids.advance.text = "Advance: " + str(self.advance)
        self.ids.ride_distance.text = 'Ride Distance: '+str(self.ride_distance) + " km"
        self.ids.duration.text = 'Travel Time: '+ str(self.duration) + " mins"
        self.ids.time_of_arrival.text = f"Driver is [color=0000ff]{str(self.time_of_arrival)}[/color] minutes away"

    def goBack(self):
        self.manager.current = 'Phome'

    def cancel_ride(self):
        cancellationFee = priceGen.cancelRide(rideID=self.rideID)
        self.manager.get_screen('cancelscreen').update_result(cancellationFee)
        self.manager.current = 'cancelscreen'


class CancellationScreen(Screen):
    def update_result(self, computed_value):
        self.ids.cancelfee.text = "Cancellation Fee: " + str(computed_value)
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
