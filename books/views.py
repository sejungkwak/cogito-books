from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView, UpdateView
from django.db.models import Q

import datetime

from .models import Category, Genre, Author, Book, Review
from .forms import BookForm, ReviewForm


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
            if sort_option == 'rating':
                qs = sorted(
                    list(qs), key=lambda a: a.get_average_rating())
            elif sort_option == '-rating':
                qs = sorted(
                    list(qs),
                    key=lambda a: a.get_average_rating(),
                    reverse=True)
            else:
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
        if self.sort and 'rating' in self.sort:
            context['total'] = len(self.get_queryset())
        else:
            context['total'] = self.get_queryset().count()
        context['search_term'] = self.query

        return context


class BookCreateView(UserPassesTestMixin,
                     SuccessMessageMixin,
                     CreateView):
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
        Save the form if it's valid.
        """
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the homepage after adding a book.
        """
        return reverse_lazy('home')


class BookUpdateView(UserPassesTestMixin,
                     SuccessMessageMixin,
                     UpdateView):
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


class BookDeleteView(UserPassesTestMixin,
                     DeleteView):
    """
    A view to allow the superuser to delete book data.
    """
    model = Book
    template_name = 'books/delete_book.html'

    def test_func(self):
        """
        Check if the logged-in user is the superuser.
        """
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        """
        Delete a book from the database as requested by the superuser.
        """
        object = self.get_object()
        messages.success(request, 'The book has been successfully deleted.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect to the homepage after updating a book.
        """
        return reverse_lazy('home')


class BookDetailView(DetailView):
    """
    A view to display the details of a requested book
    and it's reviews. Handle the review's post request.
    """
    model = Book
    template_name = 'books/book_detail.html'

    def get(self, request, *arg, **kwargs):
        """
        Retrieve an individual book, details and it's reviews.
        """
        pk = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=pk)
        average_ratings = book.get_average_rating()
        num_of_reviewers = book.number_of_reviews()
        all_ratings = book.reviews.exclude(content=True)
        all_reviews = book.reviews.exclude(content='')
        reviews_excl_user = all_reviews.exclude(reviewer=request.user)
        reviews = reviews_excl_user.order_by('-created_at')[:4]
        has_rating = None
        user_review = None
        new_page_needed = False
        # Check if the user has already given a rating without a review.
        if all_ratings.filter(reviewer=request.user):
            for field in all_ratings.filter(reviewer=request.user):
                has_rating = field.rating
        # If the user has already written a review for the book,
        # the text input box does not display.
        if all_reviews.filter(reviewer=request.user):
            user_review = all_reviews.filter(reviewer=request.user).values()[0]
        # If the number of reviews is more than 4(excluding current user's review),
        # display a link to a separate review page.
        if all_reviews.count() > 4:
            new_page_needed = True

        return render(
            request,
            self.template_name,
            {
                'book': book,
                'average_ratings': average_ratings,
                'num_of_reviewers': num_of_reviewers,
                'reviews': reviews,
                'new_page_needed': new_page_needed,
                'has_rating': has_rating,
                'user_review': user_review,
                'new_review': True,
                'review_form': ReviewForm()
            }
        )

    def post(self, request, *arg, **kwargs):
        """
        Save the review and redirect back to the same page.
        """
        pk = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=pk)
        review_form = ReviewForm(data=request.POST)
        all_ratings = book.reviews.all()
        has_rating = False
        if all_ratings.filter(reviewer=request.user):
            has_rating = True

        if review_form.is_valid():
            form_data = {
                'new_rating': request.POST['rating'],
                'new_content': request.POST['content']
            }
            # If the user has already given a rating, override the values.
            if has_rating:
                all_ratings.filter(
                    reviewer=request.user).update(
                    rating=form_data['new_rating'],
                    content=form_data['new_content'],
                    updated_at=datetime.datetime.now())
                messages.success(
                    request, 'Your rating has been successfully updated.')
            else:
                review_form.instance.reviewer = request.user
                review = review_form.save(commit=False)
                review.book = book
                review.save()
                messages.success(
                    request, 'Your review/rating has been successfully added.')
        else:
            messages.error(request, 'Your form is invalid.')
            review_form = ReviewForm()

        return HttpResponseRedirect(
            reverse_lazy(
                'book_detail', kwargs={
                    'pk': pk}))


class ReviewListView(ListView):
    """
    A view to display a list of reviews for a book.
    """
    model = Review
    template_name = 'books/reviews.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().filter(
            book__id=self.kwargs['pk']).exclude(
            content='')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.get_queryset()
        book = reviews[0].book
        num_of_reviews = reviews.count()
        context['book'] = book
        context['num_of_reviews'] = num_of_reviews
        return context


class ReviewUpdateView(UserPassesTestMixin,
                       SuccessMessageMixin,
                       UpdateView):
    """
    A view to allow the users to update their reviews.
    """
    model = Review
    template_name = 'books/book_detail.html'
    form_class = ReviewForm
    success_message = 'Your review has been successfully updated!'

    def test_func(self):
        """
        Check if the user is the owner of the review.
        """
        if self.get_object().reviewer == self.request.user:
            return True

    def get(self, request, *args, **kwargs):
        """
        Retrieve the book that the review belongs.
        """
        book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        average_ratings = book.get_average_rating()
        num_of_reviewers = book.number_of_reviews()
        reviews = book.reviews.all().exclude(
            pk=self.kwargs.get('pk')).order_by('-created_at')
        review = book.reviews.filter(pk=self.kwargs.get('pk')).first()
        reviews_with_content = book.reviews.exclude(content='')
        reviews_with_content = reviews_with_content.order_by('-created_at')[:5]

        return render(
            request,
            self.template_name,
            {
                'book': book,
                'average_ratings': average_ratings,
                'num_of_reviewers': num_of_reviewers,
                'reviews': reviews_with_content,
                'review': review,
                'new_review': False,
                'review_form': ReviewForm(instance=review)
            }
        )

    def get_success_url(self):
        """
        Render the book detail page after saving the edited review.
        """
        return reverse_lazy(
            'book_detail', kwargs={
                'pk': self.kwargs['book_id']})


class ReviewDeleteView(UserPassesTestMixin, DeleteView):
    """
    Delete an individual review.
    """
    model = Review
    template_name = 'books/delete_review.html'

    def test_func(self):
        """
        Check if the user is the owner of the review.
        """
        if self.get_object().reviewer == self.request.user:
            return True

    def delete(self, request, *args, **kwargs):
        """
        Delete a review from the database.
        """
        object = self.get_object()
        messages.success(
            request, 'Your review has been successfully deleted.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """
        Render the book detail page after deleting the review.
        """
        return reverse_lazy(
            'book_detail', kwargs={
                'pk': self.kwargs['book_id']})
