from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    The OrderLineItem section for the order panel.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    The Order panel for the admin site.
    """
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'subtotal',
        'paid_points',
        'grand_total')
    fields = (
        'order_status',
        'order_number',
        'date',
        'full_name',
        'email',
        'phone_number',
        'country',
        'postcode',
        'town_or_city',
        'address_line_1',
        'address_line_2',
        'county',
        'delivery_cost',
        'subtotal',
        'paid_points',
        'grand_total')
    list_display = (
        'order_status',
        'order_number',
        'date',
        'full_name',
        'subtotal',
        'delivery_cost',
        'grand_total')
