from datetime import datetime
import email
from multiprocessing import context
from sqlite3 import complete_statement
from subprocess import check_output
from unicodedata import category
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Checkings, Roomtype,Room,Booking
import random
import string
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
purchasekey='bohamiakey20'
def hotelhome(request):
    return HttpResponse('home page')
def book(request):
    return render(request,'hotel/booking.html')
def payment(request):
    if request.method=='POST':
        category=request.POST.get('roomcategory')
        num_rooms=request.POST.get('numberofrooms')
        dayfrom=request.POST.get('bookfrom')
        dayto=request.POST.get('booktill')
        d1=datetime.strptime(dayfrom,"%Y-%m-%d").day
        d2=datetime.strptime(dayto,"%Y-%m-%d").day
        days=d2-d1
        a=Roomtype.objects.all().filter(room_type__contains=category)[0]
        totalprice= a.price_per_night * float(days) * float(num_rooms)

        request.session['roomcategory']=category
        request.session['numberofrooms']=num_rooms
        request.session['num_of_days']=days
        request.session['dayfrom']=dayfrom
        request.session['daytill']=dayto
        request.session['totalprice']=totalprice


        context={
            'totalprice':totalprice
        }
        
        return render(request,'hotel/payment.html',context)
    else:
        return redirect('book')

def confirm(request):
    if request.method=='POST':

        
            firstname=request.POST.get('fname')
            lastname=request.POST.get('lname')
            email=request.POST.get('email')
            address=request.POST.get('address')

            request.session['fname']=firstname
            request.session['lname']=lastname
            request.session['email']=email
            request.session['address']=address

             # send email
                      
            subject = f'Hi {firstname}Thank you for your Booking' 
            message = f'To Complete booking enter the purchase pin {purchasekey}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail( subject, message, email_from, recipient_list )
            print(  'A')
            context={'email':email}

            return render(request,'hotel/confirm.html')   
    else:
          return redirect('book') 
          print(  'A1') 

def validate(request):
    if request.method=='POST':
        userkey=request.POST.get('userkey')
        
        if userkey == purchasekey:
            bookingitem=Booking()
            bookingitem.customer=f"{request.session['fname']} {request.session['lname']} "
            a=Roomtype.objects.all().filter(room_type__contains=request.session['roomcategory'])[0]
            bookingitem.room_type=a
            bookingitem.number_of_rooms=request.session['numberofrooms'] 
            bookingitem.Date_in=request.session['dayfrom'] 
            bookingitem.Date_out=request.session['daytill'] 

            
            bookingitem.email=request.session['email'] 
            bookingitem.address=request.session['address'] 
            bookingitem.book_price=request.session['totalprice'] 
            bookingitem.booking_complete=True

            bookingitem.save()


              # send email
                      
            subject = f'Hi {bookingitem.customer}. Your booking summary' 
            message =f'Welcome to the Bohamia Hotel and resort. Your visit is scheduled from {bookingitem.Date_in} to {bookingitem.Date_out}. Total cost of {bookingitem.book_price}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [bookingitem.email,]
            send_mail( subject, message, email_from, recipient_list )
            main=10
            
             
            
            return render(request,'hotel/validate.html', {'main':main})
        else:
            return redirect('confirm')


def room(request):
    rooms=Roomtype.objects.all()
    

    return render(request,'hotel/rooms.html',{'rooms':rooms})

def roomdetail(request,type1):
    room=Roomtype.objects.all().filter(room_type__contains=type1)[0]
    print(14)
    print(room.room_type)
    
    return render(request,'hotel/roomdetail.html' ,{'room':room})

def checkin(request):
    if request.method=='POST':
        search=request.POST.get('checksearch')
        bookinglist=Booking.objects.all().filter(customer__contains=search)
        bookings=bookinglist.filter(check_in_status=False)

        context={
            'bookings':bookings,
            'search':search
        }
        
        return render (request,'hotel/checkin.html', context)
       

    return render (request,'hotel/checkin.html')  


def addcheckin(request):
    if request.method=='POST':
        check_status=request.POST.get('checkin?')
        bookingid=request.POST.get('booking_id')
        assigned_room=request.POST.get('room_number')
        roomcategory=request.POST.get('booking_roomtype')

       
        checked_booking=Booking.objects.all().filter(id=bookingid)[0]
        room=Roomtype.objects.all().filter(room_type__contains=roomcategory)[0]
        booked_rooms= checked_booking.number_of_rooms
        print('ye ye ye')
        print(room)
        if room.number-booked_rooms>0:
            checked_booking.check_in_status=check_status
          
            
            checked_booking.save()
            checkindetails=Checkings()
            checkindetails.booking=checked_booking
            checkindetails.check_in=True
            checkindetails.room_category=checked_booking.room_type
            checkindetails.checkin_room=assigned_room
            checkindetails.checkout_date=datetime.now()
        
            checkindetails.save()
            print('ye ye ye')
            print(room)
            room.number=room.number-booked_rooms
            room.save()

            bookings=Checkings.objects.all().filter(check_in=True)
            context={
                'bookings':bookings,   
            }
            
            
            return redirect('addcheckin')
        else:
            return HttpResponse(' <h2 style=" color:red; padding:5%;"> Insufficiently available rooms of type  </h2>')
            
    else:
         bookinglist=Checkings.objects.all().filter(check_in=True) #checked in
         bookingsout=bookinglist.filter(check_out_status=True).order_by('-checkout_date') # checked in and  checked out 
         bookingsin=bookinglist.filter(check_out_status=False).order_by('-checkin_date')# checked in and not checked out

         context={
            'bookingsout':bookingsout,
            'bookingsin':bookingsin,  
        }


    return render (request,'hotel/addcheckin.html', context) 

def checkout(request):
    if request.method =='POST':
        checkout_status=request.POST.get('checkout?')
        itemid=request.POST.get('checking_id')
      
        checkout_item=Checkings.objects.all().filter(id=itemid)[0]
        
        
        print(checkout_item)
        checkout_item.check_out_status=True
        checkout_item.checkout_date=datetime.now()
        checkout_item.save()
    return redirect('addcheckin')   




        
