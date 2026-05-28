from django import forms
from .models import Comment

class TicketForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea , required=True)
    name = forms.CharField(max_length=250 , required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11 , required=True)
    subject = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone :
            if not phone.isnumeric():
                raise forms.ValidationError('Phone number must be number')
            else :
                return phone

class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name :
            if len(name) < 3 :
                raise forms.validationError("Name must be at least 3 characters")
            return name
    class Meta :
        model = Comment
        fields = ['name' , 'body']