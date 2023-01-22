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
    total = 0

    for item_id, quantity in basket.items():
        book = get_object_or_404(Book, pk=item_id)
        item_count += quantity
        total += book.price * quantity
        basket_items.append({
            'book': book,
            'item_id': item_id,
            'quantity': quantity,
        })

    context = {
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'national_delivery_cost': settings.NATIONAL_DELIVERY_COST,
        'international_delivery_percentage': settings.INTERNATIONAL_DELIVERY_PERCENTAGE,
        'base_international_delivery_cost': settings.BASE_INTERNATIONAL_DELIVERY_COST,
        'basket_items': basket_items,
        'item_count': item_count,
        'total': total
    }

    return context
