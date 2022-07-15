from django.contrib import admin
from .models import Booking,Roomtype,Room,Checkings

# Register your models here.
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Roomtype)
admin.site.register(Checkings)