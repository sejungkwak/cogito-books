from django import forms
from django.contrib.auth.models import User
from .models import Profile
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserUpdateForm(forms.ModelForm):
    """
    A form to update Django User model data.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ProfileForm(forms.ModelForm):
    """
    A form to update Profile model data.
    """
    class Meta:
        model = Profile
        exclude = ('user', 'joined', 'loyalty_points')
        widgets = {
            'default_phone_number': PhoneNumberPrefixWidget(
                attrs={
                    'class': 'form-control phonenumber'}),
            'dob': forms.DateInput(
                attrs={
                    'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        labels = {
            'default_full_name': 'Full name',
            'default_phone_number': 'Phone number',
            'default_address_line_1': 'Address line 1',
            'default_address_line_2': 'Address line 2',
            'default_town_or_city': 'Town/City',
            'default_county': 'County/State',
            'default_postcode': 'postcode/ZIP',
            'default_country': 'Country',
            'dob': 'Date of Birth',
        }
        for field in self.fields:
            self.fields[field].label = labels[field]
