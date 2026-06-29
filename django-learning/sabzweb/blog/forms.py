from django import forms
from django.contrib.auth.models import User

from .models import Comment , Post ,Account

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

class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if not len(name) > 3 :
                raise forms.ValidationError("Name must have at least 3 letters!")
        return name

    def clean_body(self):
        body = self.cleaned_data['body']
        if body :
            if not len(body) > 2 :
                raise forms.ValidationError("Comment must have at least 2 letters!")
            return body
    class Meta :
        model = Comment
        fields = ['name' , 'body']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Enter Your Name :' , 'required' : True , 'class' : 'name'}) ,
            'body' : forms.Textarea(attrs={'placeholder' : 'Enter Your Comment :' , 'class' : 'comment_body'})
        }

class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="Image1")
    image2 = forms.ImageField(label="Image2")

    class Meta:
        model = Post
        fields = ['title' , 'description' , 'reading_time' , 'category']

class SearchForm (forms.Form):
    query = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100 , required=True)
    password = forms.CharField(widget=forms.PasswordInput , required=True , max_length=250)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput , required=True , max_length=20)
    password2 = forms.CharField(widget=forms.PasswordInput , required=True , max_length=20)
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' , 'email' ]
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match!")
        return cd['password2']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio' , 'date_of_birth' , 'job']
