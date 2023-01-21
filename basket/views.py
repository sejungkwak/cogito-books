from django.shortcuts import redirect, reverse, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View

from books.models import Book


class AddToBasketView(View):
    """
    A view to add a quantity of the specified book to the basket.
    """

    def post(self, request, pk, *args, **kwargs):
        """
        Handle the post request - Get the requested book and
        add it to the session storage.
        """
        book = get_object_or_404(Book, id=pk)
        quantity = int(request.POST.get('quantity'))
        basket = request.session.get('basket', {})

        if str(pk) in list(basket.keys()):
            basket[str(pk)] += quantity
        else:
            basket[str(pk)] = quantity
        messages.success(
            request,
            f'{book.title} has successfully been added to your basket')

        request.session['basket'] = basket

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class EditBasketView(View):
    """
    A view to adjust the quantity of the specified book
    to the specified amount.
    """

    def post(self, request, pk, *args, **kwargs):
        """
        Save the updated quantity.
        """
        book = get_object_or_404(Book, id=pk)
        quantity = int(request.POST.get('quantity'))
        basket = request.session.get('basket', {})

        if quantity > 0:
            basket[pk] = quantity
        else:
            basket.pop(pk)

        request.session['basket'] = basket

        return redirect(reverse('view_basket'))


class RemoveFromBasketView(View):
    """
    A view to remove the specified book from the basket.
    """

    def post(self, request, pk, *args, **kwargs):
        """
        Delete the book from the basket.
        """
        try:
            book = get_object_or_404(Book, id=pk)
            basket = request.session.get('basket', {})
            basket.pop(str(pk))
            request.session['basket'] = basket
            messages.success(
                request,
                f'{book.title} has successfully been removed from your basket')
        except Exception as e:
            messages.error(request, f'Error removing item: {e}')

        return redirect(reverse('view_basket'))
