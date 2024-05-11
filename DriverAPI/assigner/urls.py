from django.urls import path
from . import views
from django.urls import register_converter

class FloatConverter:
    regex = r"[-+]?\d*\.\d+|\d+"

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')


urlpatterns = [
    path('driver/', views.crudDriver.as_view(), name='drivers'),
    path('user/', views.crudUser.as_view(), name='user'),
    path('ride/', views.crudRides.as_view(), name='rides'),
    path('ride_request/', views.crudAssigner.as_view(), name='ride_request')
]