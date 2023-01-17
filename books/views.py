from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.db.models import Q

import datetime

from .models import Category, Genre, Book
from .forms import BookForm


class BookListView(ListView):
    """
    A view to display a requested list of books, and
    handle sorting and search queries.
    """
    model = Book
    template_name = 'books/books.html'
    paginate_by = 16
    query = None
    sort = None
    direction = None

    def get_sort_option(self):
        """
        Get a sort option that a user has selected.
        """
        if 'sort' in self.request.GET:
            self.sort = self.request.GET['sort']

        if 'direction' in self.request.GET:
            self.direction = self.request.GET['direction']
            if self.direction == 'desc':
                self.sort = f'-{self.sort}'

        return self.sort

    def get_queryset(self):
        """
        Get queryset as requested by a user.
        """
        req_list = None
        sort_option = self.get_sort_option()

        if 'q' in self.request.GET:
            self.query = self.request.GET['q']
            queries = Q(
                title__icontains=self.query) | Q(
                author__full_name__icontains=self.query) | Q(
                publisher__icontains=self.query) | Q(
                isbn10__icontains=self.query) | Q(
                isbn13__icontains=self.query) | Q(
                desc__icontains=self.query)
            qs = super().get_queryset().filter(queries).distinct()

        if 'list' in self.request.GET:
            req_list = self.request.GET['list']

        if req_list in list(
            Category.objects.values_list(
                'name', flat=True)):
            qs = super().get_queryset().filter(category__name=req_list)
        elif req_list in list(
            Genre.objects.values_list(
                'name', flat=True)):
            qs = super().get_queryset().filter(genre__name=req_list)
        elif req_list == 'sale':
            qs = super().get_queryset().filter(discount_rate__gt=0)
        elif req_list == 'bestsellers':
            qs = super().get_queryset().order_by('-amount_sold')[:100]
        elif req_list == 'new_releases':
            qs = super().get_queryset().filter(
                pub_date__gt=datetime.date.today() -
                datetime.timedelta(
                    days=30)).order_by('-pub_date')
        elif 'q' not in self.request.GET:
            qs = super().get_queryset().all()

        if sort_option:
            qs = qs.order_by(sort_option)

        return qs

    def get_context_data(self, **kwargs):
        """
        Get a context and add extra information to use in the template.
        """
        context = super().get_context_data(**kwargs)
        req_list = None

        if 'list' in self.request.GET:
            req_list = self.request.GET['list']
            context['list'] = req_list

        if req_list in list(
            Category.objects.values_list(
                'name', flat=True)):
            context['title'] = Category.objects.values_list(
                'friendly_name', flat=True).get(name=req_list)
        elif req_list in list(
            Genre.objects.values_list(
                'name', flat=True)):
            context['title'] = Genre.objects.values_list(
                'friendly_name', flat=True).get(name=req_list)
        elif req_list == 'sale':
            context['title'] = 'Sale'
        elif req_list == 'bestsellers':
            context['title'] = 'Bestsellers'
        elif req_list == 'new_releases':
            context['title'] = 'New Releases'
        else:
            context['title'] = 'All Books'

        if self.sort and self.sort[0] == '-':
            self.sort = self.sort[1:]

        if self.sort is not None:
            context['sort_params'] = (f'&sort={self.sort}&direction='
                                      f'{self.direction}')
        context['sort'] = self.sort
        context['direction'] = self.direction
        context['current_sorting'] = f'{self.sort}_{self.direction}'
        context['total'] = self.get_queryset().count()
        context['search_term'] = self.query

        return context


class BookCreateView(CreateView,
                     UserPassesTestMixin,
                     SuccessMessageMixin):
    """
    A view to handle the form to add a book to the database.
    """
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_message = 'This book has been successfully added!'

    def test_func(self):
        """
        Check if the logged-in user is the superuser.
        """
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        Get a context and add extra information to use in the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add a Book'
        context['button_content'] = 'Add'
        return context

    def form_valid(self, form):
        """
        Save the form with the value of the logged-in user.
        """
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the homepage after adding a book.
        """
        return reverse_lazy('home')

class BookUpdateView(UpdateView,
                     UserPassesTestMixin,
                     SuccessMessageMixin):
    """
    A view to allow the superuser to update book data.
    """
    model = Book
    template_name = 'books/add_book.html'
    form_class = BookForm
    success_message = 'This book has been successfully updated!'

    def test_func(self):
        """
        Check if the logged-in user is the superuser.
        """
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        Get a context and add extra information to use in the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit a Book'
        context['button_content'] = 'Update'
        return context

    def get_success_url(self):
        """
        Redirect to the homepage after updating a book.
        """
        return reverse_lazy('home')
