from django.shortcuts import render
from django.views.generic.list import ListView

from books.models import Book


class BookListView(ListView):
    """
    Display a list of bestsellers and new releases.
    """
    model = Book
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        """
        Filter books by the number of sales and publication date.
        """
        context = super().get_context_data(**kwargs)
        context['bestsellers'] = Book.objects.order_by('-amount_sold')[:10]
        context['new_releases'] = Book.objects.order_by('-pub_date')[:10]

        return context
