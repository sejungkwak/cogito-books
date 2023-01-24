from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from books.models import Book


class Profile(models.Model):
    """
    A user profile model for maintaining default delivery information,
    order history and change password.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=254, null=True, blank=True)
    default_phone_number = PhoneNumberField(
        null=True, blank=True, default='IE')
    default_address_line_1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_address_line_2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True, default='IE')
    dob = models.DateField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    loyalty_points = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    """
    A wishlist model for users to save books.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True, related_name='wishlist')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user.username}\'s wishlist'

    def number_of_books(self):
        return self.books.count()


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    """
    Create a profile for a new user or update it.
    """
    if created:
        Profile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()
