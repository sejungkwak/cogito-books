from django.contrib import admin
from .models import Genre, Author, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Genre panel for the admin site
    """
    list_display = (
        'friendly_name',
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Author panel for the admin site
    """
    list_display = (
        'full_name',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Book panel for the admin site
    """
    list_display = (
        'title',
        'genre',
        'all_authors',
        'price',
        'amount_sold'
    )

    def all_authors(self, obj):
        return ' & '.join([a.full_name for a in obj.author.all()])
