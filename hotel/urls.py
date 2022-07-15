from django.urls import path

from . import views


urlpatterns = [
   
    path('', views.hotelhome),
    path('book/', views.book, name='book'),
    path('payment/', views.payment, name='payment'),
    path('confirm/', views.confirm, name='confirm'),
    path('validate/', views.validate, name='validate'),
    path('rooms/', views.room, name='rooms'),
    path('room/<slug:type1>/', views.roomdetail, name='roomdetail'),
    path('checkin/', views.checkin, name='checkin'),
    path('addcheckin/', views.addcheckin, name='addcheckin'),
    path('checkout/', views.checkout, name='checkout'),
 
]