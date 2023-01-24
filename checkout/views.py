from django.shortcuts import (render, redirect, reverse,
                              get_object_or_404, HttpResponse)
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.views.decorators.http import require_POST

from .models import Order, OrderLineItem
from .forms import OrderForm
from profiles.models import Profile
from books.models import Book
from basket.contexts import basket_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    Modify Stripe's PaymentIntent method to add the save delivery
    information checkbox checked to the metadata key.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


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

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = self.stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                point_balance = profile.loyalty_points
                order_form = OrderForm(initial={
                    'email': profile.user.email,
                    'full_name': profile.default_full_name,
                    'phone_number': profile.default_phone_number,
                    'address_line_1': profile.default_address_line_1,
                    'address_line_2': profile.default_address_line_2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'postcode': profile.default_postcode,
                    'country': profile.default_country
                })
            except Profile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        context = {
            'point_balance': point_balance,
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()

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

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            order.profile = profile
            order.save()

        if save_info:
            profile_data = {
                'default_full_name': order.full_name,
                'default_phone_number': order.phone_number,
                'default_address_line_1': order.address_line_1,
                'default_address_line_2': order.address_line_2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
            }
            profile_form = ProfileForm(profile_data, instance=profile)
            if profile_form.is_valid():
                profile_form.save()

        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

        if 'basket' in request.session:
            del request.session['basket']

        context = {
            'order': order,
        }

        return render(request, self.template, context)
