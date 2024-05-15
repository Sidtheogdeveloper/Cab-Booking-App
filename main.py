from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import csv, os
import auth
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview import MapView
from kivy.uix.dropdown import DropDown
import map
import API_Functions as db
import update_API_functions as update_db

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
    
    def update_marker(self, marker, lat, long):
        marker.lat= lat
        marker.lon= long

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
