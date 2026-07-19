from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100 , required=True , label="Username Or Phone Or Email :")
    password = forms.CharField(widget=forms.PasswordInput , required=True , max_length=250 , label="Password")