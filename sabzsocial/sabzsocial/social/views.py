from django.contrib.auth import logout
from django.shortcuts import render , redirect
from django.http import HttpResponse
# Create your views here.

def profile(request):
    return HttpResponse("Logged in Successfully.")

def log_out(request):
    logout(request)
    return redirect('social:login')