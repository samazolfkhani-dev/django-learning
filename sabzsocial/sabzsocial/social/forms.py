from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100 , required=True , label="Username Or Phone Or Email :")
    password = forms.CharField(widget=forms.PasswordInput , required=True , max_length=250 , label="Password")

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput , required=True , max_length=20)
    password2 = forms.CharField(widget=forms.PasswordInput , required=True , max_length=20)
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' , 'email' , 'date_of_birth' , 'bio' , 'job' , 'phone' , 'photo']
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match!")
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists!")
        return phone

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' , 'email' , 'date_of_birth' , 'bio' , 'job' , 'phone' , 'photo']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id = self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id = self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists!")
        return phone

