from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import UserContactForm


def contact_us(request):
    """
    Display the contact form and handle a user's input.
    """
    template = 'helpcentre/contact_us.html'

    if request.method == 'POST':
        form = UserContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            to_email = settings.DEFAULT_FROM_EMAIL
            form.save()
            body = f'{str(message)}\n\nReply to {str(email)}'
            try:
                send_mail(subject, body, f'{name} <{email}>', [to_email])
                messages.success(
                    request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(
                    request,
                    'There was an error trying to send your message. \
                        Please try again later.')
        else:
            messages.error(
                request,
                'There were errors on the form. Please double check \
                    and try again.')

    form = UserContactForm()

    return render(request, template, {'form': form})
