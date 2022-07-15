import re
from django.db import models
from django.contrib.auth.models import User
import random 
from ckeditor.fields import RichTextField  


# Create your models here
# 
# 
room_choices = (
    ("single", "single"),
    ("double", "double"),
    ("premium", "premium"),
   
)
def room_num_generator():
    
    number = random.randint(1000,9999)
    return number

class Roomtype(models.Model):


    room_type = models.CharField(max_length=9,
                  choices=room_choices,
                  default="single" )
    number=models.IntegerField()
    price_per_night=models.FloatField()
    description=RichTextField(blank=True,null=True)
    amenities=RichTextField(blank=True,null=True)
    image1=models.FileField(null=True)
    image2=models.FileField(null=True)
    image3=models.FileField(null=True)
    image4=models.FileField(null=True)

    def snippet(self):
        return self.description[:50]

    def __str__(self):
        return self.room_type

class Room(models.Model):
    room_category=models.ForeignKey(Roomtype, related_name='roomcategory' , on_delete=models.CASCADE)
    room_number=models.CharField(max_length=10, unique=True, default=room_num_generator)
    book_status= models.BooleanField(default=False)
    
    
    @property
    def price(self):
        room_price=Roomtype.price_per_night
        return room_price
    def __str__(self):
        return f' Info for room number {self.room_number}'
    


class Booking(models.Model):
    customer= models.CharField(max_length=50,null=True) 
    email= models.EmailField(max_length=50,null=True) 
    address= models.CharField(max_length=50,null=True)
    room_type= models.ForeignKey(Roomtype, on_delete=models.CASCADE,)
    number_of_rooms=models.IntegerField(null=True)
    Date_in= models.DateField(null=True)
    Date_out= models.DateField(null=True)
    book_price=models.FloatField(null=True)
    booking_complete= models.BooleanField(default=False)
    check_in_status=models.BooleanField(default=False  , null=True)
    
    

    @ property
    def bookprice(self):
        pricetotal=self.number_of_rooms * self.room_number.price
        return pricetotal
    def __str__(self):
        return f' Booking for {self.customer}'


class Checkings(models.Model):
    
    booking=models.OneToOneField(Booking, related_name='booking', on_delete=models.CASCADE)
    #checkin_room=models.ForeignKey(Room, related_name='checkinroom', on_delete=models.CASCADE)
    checkin_room=models.CharField(max_length=100 )
    checkin_date=models.DateTimeField(auto_now_add=True)
    checkout_date=models.DateTimeField()
    check_in=models.BooleanField(default=False, null=True)
    
    check_out_status=models.BooleanField(default=False  ,blank=True, null=True)

    def __str__(self):
        return f' Check in for {self.booking.customer}'



