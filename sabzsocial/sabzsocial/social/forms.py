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

class TicketForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea , required=True)
    name = forms.CharField(max_length=100 , required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11 , required=True)
    subject = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("Phone number must have digits!")
        return phone


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description' , 'tags']


class CommentForm(forms.ModelForm):
    def clean_body(self):
        body = self.cleaned_data['body']
        if body :
            if not len(body) > 2 :
                raise forms.ValidationError("Comment must have at least 2 letters!")
            return body
    class Meta :
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder' : 'Enter Your Comment :' , 'class' : 'comment_body'})
        }

