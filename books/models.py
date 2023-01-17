from django.db import models
from django.core.validators import MinLengthValidator


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
    pages = models.IntegerField()
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
    amount_sold = models.IntegerField(default=0.00)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
