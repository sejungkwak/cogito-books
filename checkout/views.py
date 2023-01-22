from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .models import Order
from .forms import OrderForm
from basket.contexts import basket_contents

import stripe


def checkout(request):
    """
    A view to handle the checkout-related request.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "Your basket is currently empty.")
        return redirect(reverse('book_list'))

    current_basket = basket_contents(request)
    total_excl_delivery = current_basket['total']
    stripe_total = round(total_excl_delivery * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )
    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
    }

    return render(request, template, context)
