from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
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

        request.session['basket'] = basket

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
