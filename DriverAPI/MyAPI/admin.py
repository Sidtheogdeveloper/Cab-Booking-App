from django.contrib import admin
from .models import Driver, User, Ride

# Register your models here.
admin.site.register(Driver)
admin.site.register(User)
admin.site.register(Ride)