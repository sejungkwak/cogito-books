from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Genre, Author, Book, Review, Recommendation


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Genre panel for the admin site
    """
    list_display = (
        'category',
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
    search_fields = ['title']

    def all_authors(self, obj):
        return ' & '.join([a.full_name for a in obj.author.all()])


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Review panel for the admin site
    """
    list_display = (
        'book',
        'reviewer',
        'rating',
        'created_at'
    )


@admin.register(Recommendation)
class RecommendationAdmin(SummernoteModelAdmin):
    """
    Recommendation(book of the month) panel for the amdin site
    """
    list_display = (
        'book',
        'title',
        'created_at',
        'featured_year',
        'featured_month',
        'published'
    )
    search_fields = ['title']
    summernote_fields = ('content',)
