from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.generic.list import ListView

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

from books.models import Book, Recommendation
import json


class BookListView(ListView):
    """
    Display a list of bestsellers and new releases and the book of the month.
    """
    model = Book
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        """
        Filter books by the number of sales and publication date.
        """
        context = super().get_context_data(**kwargs)
        try:
            published_book_of_month = \
                Recommendation.objects.get(published=True)
            if published_book_of_month:
                context['book_of_the_month'] = published_book_of_month
        except Recommendation.DoesNotExist:
            context['book_of_the_month'] = None
        context['bestsellers'] = Book.objects.order_by('-amount_sold')[:10]
        context['new_releases'] = Book.objects.order_by('-pub_date')[:10]

        return context


def subscribe_to_newsletter(request):
    """
    A view to allow users to subscribe email newsletter using Mailchimp.
    """
    api_key = settings.MC_API_KEY
    audience_id = settings.MC_AUDIENCE_ID
    redirect_url = request.POST.get('redirect_url')

    if request.method == 'POST':
        email = request.POST['email']

        mailchimpClient = Client()
        mailchimpClient.set_config({
            "api_key": api_key,
        })

        userInfo = {
            "email_address": email,
            "status": "subscribed",
        }

        try:
            mailchimpClient.lists.add_list_member(audience_id, userInfo)
            messages.success(request, 'Thank you for subscribing!')
        except ApiClientError as error:
            error_message = json.loads(error.text)['detail']
            messages.error(request, f'{error_message}')

    return redirect(redirect_url)
