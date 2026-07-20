from django.contrib.auth import logout
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def profile(request):
    return HttpResponse("Logged in Successfully.")

def log_out(request):
    logout(request)
    return redirect('social:login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request , 'registration/register_done.html' , {'user':user})
    else :
        form = RegisterForm()
    return render(request, 'forms/register.html' , {'form':form})

@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST , request.FILES , instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('social:profile')
    else:
        user_form = EditUserForm(instance=request.user)
    context = {
        'user_form':user_form,
    }
    return render(request , 'registration/edit_user.html' , context)