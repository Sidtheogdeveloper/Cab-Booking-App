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
        with open('userdetails.csv', 'r') as f:
            reader= csv.reader(f)
            p=1
            for i in reader:
                if email in i and password in i:
                    self.otp= auth.gen_otp()
                    response= auth.mail(email, i[0], self.otp)
                    self.otp='123'
                    f= open("recentPlogin.csv", 'w')
                    writer= csv.writer(f)
                    writer.writerow([email, password]) 
                    f.close()
                    if response== "error":
                        widget.text= "Some Error occurred"
                        break
                    widget.text="OTP sent to your Mail"
                    break
                elif email in i and password not in i:
                    p=0

            else:
                if p==0:
                    widget.text= 'Password Incorrect'
                else:
                    widget.text= 'email doesn\'t exist'

    def __verify__(self, otp, widget):  
        if self.otp==otp:
            widget.text= 'OTP Verified'
            self.manager.current ='Phome'
        else:
            widget.text= 'Incorrect OTP'

class PassengerSP(Screen):
    def __enter_data__(self, name, user, email,pwd ,cpwd, widget):  
        f= open("userdetails.csv", "a", newline= '')
        writer = csv.writer(f)
        g= open("userdetails.csv", 'r')
        reader= csv.reader(g)
        if pwd==cpwd:
            for i in reader:
                if user in i or email in i:
                    widget.text= "User already exists"
                    break
            else:
                self.otp= auth.gen_otp()
                auth.mail(email, name, self.otp)
                widget.text= "OTP Sent to your Email ID"
                writer.writerow([name, email ,user, pwd])  
        f.close()
        g.close()

    def verify_otp(self, otp, widget):
        if  otp == self.otp:
            widget.text= "OTP verified"
        else:
            widget.text= 'Invalid OTP'

class ForgotpwdPas(Screen):
    def __verify__(self, email, widget):
        f= open('userdetails.csv', 'r')
        data= csv.reader(f)
        for i in data:
            if len(i)>0 and email in i:
                self.otp= auth.gen_otp()
                auth.pwd_change_req(email,i[0], self.otp)
                self.email= email
                widget.text= 'OTP sent to you mail'
                break
        else:
            widget.text= "Email doesn't exist"
        
    def change_pwd(self, otp, widget):
        if self.otp==otp:
            with open('fppass.csv', 'w',newline= '') as f:
                writer= csv.writer(f)
                writer.writerow([self.email])
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
            f= open('userdetails.csv', 'r')
            g= open('userdet.csv', 'w', newline='')
            p= open('fppass.csv','r')
            reader= csv.reader(f)
            writer= csv.writer(g)
            pw= csv.reader(p)
            for i in pw:
                email= i[0]
            p.close()
            for i in reader:
                x= i
                if len(x)>1 and x[1]==email:
                    x[3]=str(newpwd)
                    name= x[0]
                    writer.writerow(x)
                else:
                    writer.writerow(i)
            f.close()
            g.close()
            os.remove('userdetails.csv')
            os.rename('userdet.csv', 'userdetails.csv')
            auth.pwd_reset_info(email, name)
            widget.text= 'Password Updated'
            os.remove('fppass.csv')
            self.manager.current= 'Phome'
        else:
            widget.text= "Password doesn't match"

class PassengerHome(Screen):
    def on_text_pickup(self, prompt):
        myMap = map.API()
        suggestions = myMap.suggestionCoordinates(prompt.text)
        print(suggestions)
        self.pickup_sug= []
        for i in suggestions[:3]:
            a= location(location= i[0], coords= i[1])
            self.pickup_sug.append(a)
        self.ids.suggest1.text= suggestions[0][0]
        self.ids.suggest2.text= suggestions[1][0]
        self.ids.suggest3.text= suggestions[2][0]

    def select_option(self, suggestion,pos ,textWidget):
        try:
            textWidget.text = suggestion
            lon= self.pickup_sug[pos].coords[0]
            lat= self.pickup_sug[pos].coords[1]
            self.ids.pickup.text= self.pickup_sug[pos].location
            self.update_map_coordinates(lat, lon)
        except:
            textWidget.text= 'No text available'

    def update_map_coordinates(self, lat, lon):
        mapview = self.ids.passmap
        mapview.lat = lat
        mapview.lon = lon
    
    def set_option(self, vehicle):
        self.ids.vehicle.text = vehicle

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
