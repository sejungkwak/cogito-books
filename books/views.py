from django.shortcuts import render
from django.views.generic.list import ListView
import datetime

from .models import Genre, Book


class BookListView(ListView):
    """
    Display a list of books.
    """
    model = Book
    template_name = 'books/books.html'
    paginated_by = 16

    def get_queryset(self):
        """
        Get queryset as requested by a user.
        """
        if 'list' in self.request.GET:
            req_list = self.request.GET['list']

            if req_list in list(Genre.objects.values_list('name', flat=True)):
                return super().get_queryset().filter(genre__name=req_list)
            elif req_list == 'sale':
                return super().get_queryset().filter(discount_rate__gt=0)
            elif req_list == 'bestsellers':
                return super().get_queryset().order_by('-amount_sold')[:100]
            elif req_list == 'new_releases':
                return super().get_queryset().filter(
                    pub_date__gt=datetime.date.today() -
                    datetime.timedelta(
                        days=30))[
                    :100]
        return super().get_queryset().all()

    def get_context_data(self, **kwargs):
        """
        Get a title of the request list.
        """
        context = super().get_context_data(**kwargs)

        if 'list' in self.request.GET:
            req_list = self.request.GET['list']
            if req_list in list(Genre.objects.values_list('name', flat=True)):
                context['title'] = Genre.objects.values_list(
                    'friendly_name', flat=True).get(name=req_list)
            elif req_list == 'sale':
                context['title'] = 'Sale'
            elif req_list == 'bestsellers':
                context['title'] = 'Bestsellers'
            elif req_list == 'new_releases':
                context['title'] = 'New Releases'

        return context
