from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .models import Order
from .forms import OrderForm


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
        'order_form': order_form
    }

    return render(request, template, context)
