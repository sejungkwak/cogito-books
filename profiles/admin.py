from django.contrib import admin
from django import forms
from .models import Profile
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProfileForm(forms.ModelForm):
    class Meta:
        widgets = {
            'default_phone_number': PhoneNumberPrefixWidget(initial='IE'),
        }


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile view in the admin panel
    """
    model = Profile
    form = ProfileForm
    list_display = ('id', 'username', 'full_name', 'dob', 'joined', 'loyalty_points')

    def id(self, obj):
        return obj.id

    def username(self, obj):
        return obj.user.username

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
