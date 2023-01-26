from django import forms
from .models import UserContact

class UserContactForm(forms.ModelForm):
    """
    A form to get the user's 
    """
    class Meta:
        model = UserContact
        fields = ('subject', 'name', 'email', 'message')
