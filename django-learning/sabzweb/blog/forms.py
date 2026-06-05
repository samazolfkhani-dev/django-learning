from django import forms
from .models import Comment , Post

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


class PostForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if not len(title) > 3 :
                raise forms.ValidationError("Title must have at least 3 letters!")
            return title

    class Meta :
        model = Post
        fields = ['author' , 'title' , 'description' , 'reading_time']