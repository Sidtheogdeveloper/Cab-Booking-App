from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import csv, os
import auth
from kivy.uix.image import Image


class MainScreen(Screen):
    pass

class DriverScreen(Screen):
    pass

class Driversignup(Screen):
    def __enter_data__(self, name, user, email,vehicle,pwd ,cpwd, widget):  
        g= open("driverdetails.csv", 'r')
        reader= csv.reader(g)
        f= open("driverdetails.csv", "a")
        writer = csv.writer(f)
        if pwd==cpwd:
            for i in reader:
                if user in i or email in i:
                    widget.text= "User already exists"
                    break
            else:
                self.otp= auth.gen_otp()
                auth.mail(email, name, self.otp)
                widget.text= "OTP Sent to your Email ID"
                writer.writerow([name, email, vehicle ,user, pwd])  
        f.close()
        g.close()

    def verify_otp(self, otp, widget):
        if  otp == self.otp:
            widget.text= "OTP verified"
        else:
            widget.text= 'Invalid OTP'


class DriverLog(Screen):
    def __submit__(self, email, password, widget):
        with open('driverdetails.csv', 'r') as f:
            reader= csv.reader(f)
            for i in reader:
                if len(i)==5 and email in i and password in i:
                    self.otp= auth.gen_otp()
                    auth.mail(email, i[0], self.otp)
                    widget.text="OTP sent to your Mail"
                    break
            else:
                widget.text= 'email doesn\'t exist'

    def __verify__(self, otp, widget):  
        if self.otp==otp:
            widget.text= 'OTP Verified'
        else:
            widget.text= 'Incorrect OTP'

class PassengerSP(Screen):
    pass

class PassengerLog(Screen):
    pass

class PassengerScreen(Screen):
    pass

class Windows(ScreenManager):
    pass

kv= Builder.load_file("design.kv")

class CabBookingApp(App):
    def build(self):
        return kv

    def login(self, instance):
        pass
    def signup(self, instance):
        pass
    
if __name__ == '__main__':
    CabBookingApp().run()
