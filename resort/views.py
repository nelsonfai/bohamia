from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def amenities(request):
    return HttpResponse('Amenities')