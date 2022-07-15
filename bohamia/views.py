from django.shortcuts import render
from http.client import HTTPResponse
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

