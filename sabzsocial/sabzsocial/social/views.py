from django.contrib.auth import logout
from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from sabzsocial import settings


# Create your views here.

@login_required
def profile(request):
    user = get_object_or_404(User , pk= request.user.id)
    return render(request , 'social/profile.html' , {'user' : user})

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

def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n\n{cd['message']}"
            send_mail(cd['subject'],message,'samazolfkhani12@gmail.com',['samazolfkhani12@gmail.com'] , fail_silently=False)
            sent = True
    else:
        form = TicketForm()
    return render(
        request,'forms/ticket.html',{'form': form,'sent': sent}
    )