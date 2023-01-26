from django.contrib import admin
from .models import UserContact


@admin.register(UserContact)
class UserContactModel(admin.ModelAdmin):
    """
    The UserContact panel for the admin site.
    """
    model = UserContact
    list_display = [field.name for field in UserContact._meta.get_fields()]
