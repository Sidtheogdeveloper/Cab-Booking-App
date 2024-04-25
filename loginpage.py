from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import kivy.properties as kyprops

class LoginScreen(Widget):
    def _init_(self, **kwargs):
        super(LoginScreen, self)._init_(**kwargs)
        self.username = kyprops.ObjectProperty(None)
        self.password = kyprops.ObjectProperty(None)

    def login(self, username, password):
        # Here you can add your logic to check if the username and password are correct
        pass

class SignUpScreen(Widget):
    def _init_(self, **kwargs):
        super(SignUpScreen, self)._init_(**kwargs)
        self.username = kyprops.ObjectProperty(None)
        self.password = kyprops.ObjectProperty(None)
        self.confirm_password = kyprops.ObjectProperty(None)

    def sign_up(self, username, password, confirm_password):
        # Here you can add your logic to sign up a new user
        pass

class HomeScreen(Widget):
    pass

class BoxLayout(BoxLayout):
    def _init_(self, **kwargs):
        super(BoxLayout, self)._init_(**kwargs)
        self.login_screen = LoginScreen()
        self.sign_up_screen = SignUpScreen()
        self.home_screen = HomeScreen()
        self.add_widget(self.login_screen)
        self.add_widget(self.sign_up_screen)
        self.add_widget(self.home_screen)

    def login(self):
        self.clear_widgets()
        self.add_widget(self.login_screen)

    def sign_up(self):
        self.clear_widgets()
        self.add_widget(self.sign_up_screen)

    def home(self):
        self.clear_widgets()
        self.add_widget(self.home_screen)

class cabbookingApp(App):
    def build(self):
        return BoxLayout()
    
if __name__=="__main__":
    cabbookingApp().run()