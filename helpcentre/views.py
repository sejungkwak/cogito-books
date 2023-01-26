from django.shortcuts import render


def contact_us(request):
    """
    Display a contact form and handle a user's input.
    """

    if request.method == 'POST':
        pass