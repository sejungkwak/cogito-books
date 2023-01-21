from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .models import Order
from .forms import OrderForm

import stripe

def checkout(request):
    """
    A view to handle the checkout-related request.
    """
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "Your basket is currently empty.")
        return redirect(reverse('book_list'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': ''
    }

    return render(request, template, context)
