from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.conf import settings

from books.models import Book


def basket_contents(request):
    """
    Return a context of the basket.
    """
    basket_items = []
    item_count = 0
    basket = request.session.get('basket', {})

    for item_id, quantity in basket.items():
        book = get_object_or_404(Book, pk=item_id)
        item_count += quantity
        basket_items.append({
            'book': book,
            'item_id': item_id,
            'quantity': quantity,
        })

    context = {
        'basket_items': basket_items,
        'item_count': item_count,
    }

    return context
