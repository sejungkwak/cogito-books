from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views import View

from .models import Order, OrderLineItem
from .forms import OrderForm
from books.models import Book
from basket.contexts import basket_contents

import stripe


class CheckoutView(View):
    """
    A view to handle the checkout-related request.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    template = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        """
        Display the payment form.
        """
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is currently empty.")
            return redirect(reverse('book_list'))
        if not self.stripe_public_key:
            messages.warning(request, 'Stripe public key is missing.')

        order_form = OrderForm()

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = self.stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )

        context = {
            'order_form': order_form,
            'stripe_public_key': self.stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        """
        Handle the user's payment detail input.
        """
        basket = request.session.get('basket', {})
        current_basket = basket_contents(request)

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_line_1': request.POST['address_line_1'],
            'address_line_2': request.POST['address_line_2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()

            # Create each line item from the order.
            for item_id, quantity in basket.items():
                try:
                    book = Book.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        book=book,
                        quantity=quantity
                    )
                    order_line_item.save()
                except Book.DoesNotExist:
                    messages.error(
                        request, ('One of the books in your basket \
                                  wasn\'t found in our database. '
                                  'Please contact us for assistance.'))
                    order.delete()
                    return redirect(reverse('view_basket'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse(
                    'checkout_success',
                    args=[
                        order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
            return redirect(reverse('view_basket'))


class CheckoutSuccessView(View):
    """
    Handle successful checkouts.
    """
    template = 'checkout/checkout_success.html'

    def get(self, request, order_number, *args, **kwargs):
        save_info = request.session.get('save_info')
        order = get_object_or_404(Order, order_number=order_number)

        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

        if 'basket' in request.session:
            del request.session['basket']

        context = {
            'order': order,
        }

        return render(request, self.template, context)
