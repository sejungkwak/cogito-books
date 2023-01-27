from django.db import models
from django.db.models import Avg, PositiveIntegerField
from django.contrib.auth.models import User
from django.core.validators import (MinLengthValidator,
                                    MinValueValidator, MaxValueValidator)

from decimal import Decimal
import datetime


class Category(models.Model):
    """
    Category database model
    """
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Genre database model
    """
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        if not self.friendly_name:
            self.friendly_name = self.name.title()
        super().save(*args, **kwargs)


class Author(models.Model):
    """
    Author database model
    """
    full_name = models.CharField(max_length=254)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Book(models.Model):
    """
    Book database model
    """
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books')
    genre = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books')
    title = models.CharField(max_length=254)
    author = models.ManyToManyField(Author, related_name='books')
    desc = models.TextField()
    cover_url = models.URLField(max_length=1024, null=True, blank=True)
    cover = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.PositiveIntegerField()
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()
    lang = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=254, null=False, blank=False)
    pub_date = models.DateField()
    isbn10 = models.CharField(
        max_length=10, unique=True, validators=[
            MinLengthValidator(10)])
    isbn13 = models.CharField(
        max_length=13, unique=True, validators=[
            MinLengthValidator(13)])
    discount_rate = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    amount_sold = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_discount_price(self):
        discount = self.price * self.discount_rate
        new_price = round(Decimal(self.price - discount), 2)
        return new_price

    def number_of_reviews(self):
        return self.reviews.count()

    def get_average_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        if not self.number_of_reviews:
            avg_rating = 0
        return avg_rating


class Review(models.Model):
    """
    Review database model
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews')
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    rating = models.PositiveIntegerField(
        null=False, blank=False, default=1, validators=[
            MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer}\'s review for {self.book}'


class Recommendation(models.Model):
    """
    Recommendation model for the book of the month.
    """
    now = datetime.datetime.now()
    YEAR_CHOICES = [(y, y) for y in range(now.year, now.year + 2)]
    MONTH_CHOICES = [(m, m) for m in range(1, 13)]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='recommendations')
    title = models.CharField(max_length=254)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    featured_year = models.IntegerField(choices=YEAR_CHOICES, default=now.year)
    featured_month = models.IntegerField(
        choices=MONTH_CHOICES, default=now.month)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-featured_month', '-featured_year']

    def __str__(self):
        return f'{self.book}: Book of the month \
                 {self.featured_month}/{self.featured_year}'

    def archive(self):
        self.published = False
        self.save()
