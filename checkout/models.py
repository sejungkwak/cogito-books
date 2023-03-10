import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from books.models import Book
from profiles.models import Profile


class Order(models.Model):
    """
    Order model storing the shopper and their order information.
    """

    ORDER_STATUS = (
        ('payment accepted', 'Payment accepted'),
        ('processing', 'Processing in progress'),
        ('dispatched', 'Dispatched'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_number = models.CharField(max_length=32, null=False, editable=False)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = PhoneNumberField(null=False, blank=False)
    address_line_1 = models.CharField(max_length=80, null=False, blank=False)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(
        blank_label='Country',
        null=False,
        blank=False,
        default='IE')
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    collecting_points = models.IntegerField(null=False, blank=False, default=0)
    paid_points = models.IntegerField(null=False, blank=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    order_status = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        choices=ORDER_STATUS,
        default='payment accepted')
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default='')

    class Meta:
        ordering = ['-date']

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.subtotal = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0
        if self.subtotal < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.subtotal * \
                settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0

        self.grand_total = self.subtotal + self.delivery_cost
        if self.paid_points:
            paid_points_in_eur = round(Decimal(self.paid_points / 100), 2)
            self.grand_total = self.subtotal + \
                self.delivery_cost - paid_points_in_eur

        self.save()

    def update_collecting_points(self):
        """
        Update loyalty points a user could earn for the purchase.
        """
        self.subtotal = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0
        self.collecting_points = self.subtotal * 5
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    OrderLineItem model storing information of an individual book.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems')
    book = models.ForeignKey(
        Book,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the line item total
        and update the order total.
        """
        price = self.book.price
        if self.book.discount_rate > 0:
            price = self.book.get_discount_price()
        self.lineitem_total = price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.book.title} on order {self.order.order_number}'
