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
    total = 0
    collecting_points = 0
    redeem_points_in_eur = 0
    basket = request.session.get('basket', {})

    for item_id, quantity in basket.items():
        book = get_object_or_404(Book, pk=item_id)
        item_count += quantity
        price = book.price
        if book.discount_rate > 0:
            price = book.get_discount_price()
        total += price * quantity
        collecting_points = int(total * 5)
        basket_items.append({
            'book': book,
            'item_id': item_id,
            'quantity': quantity,
        })

    if 'points' in request.session:
        redeem_points_in_eur = round(
            Decimal(request.session['points'] / 100), 2)

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    else:
        delivery = 0

    grand_total = delivery + total - redeem_points_in_eur

    context = {
        'basket_items': basket_items,
        'item_count': item_count,
        'delivery': delivery,
        'lineitem_total': total,
        'collecting_points': collecting_points,
        'redeem_points_in_eur': redeem_points_in_eur,
        'grand_total': grand_total,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD
    }

    return context
