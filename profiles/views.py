from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Profile, Wishlist
from .forms import UserUpdateForm, ProfileForm
from books.models import Book
from checkout.models import Order


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A view displays account menu options.
    """
    template_name = 'profiles/profiles.html'
    login_url = 'account_login'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must sign in to see this page.')
            return redirect(reverse(self.login_url))
        else:
            return render(self.request, self.template_name)


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    """
    A view to edit a user's own details and default delivery address.
    """
    model = Profile
    user_form_class = UserUpdateForm
    profile_form_class = ProfileForm
    template_name = 'profiles/profile_detail.html'

    def test_func(self):
        """
        Check if the logged-in user is the owner of the account.
        """
        if self.get_object().pk == self.request.user.pk:
            return True

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve the user's profile data and display
        current values in the form.
        """
        profile = get_object_or_404(Profile, pk=pk)
        first_name = profile.user.first_name
        last_name = profile.user.last_name
        username = profile.user.username
        email = profile.user.email
        full_name = profile.default_full_name
        phone_number = profile.default_phone_number
        address_line_1 = profile.default_address_line_1
        address_line_2 = profile.default_address_line_2
        town_or_city = profile.default_town_or_city
        county = profile.default_county
        postcode = profile.default_postcode
        country = profile.default_country
        dob = profile.dob
        user_form = self.user_form_class
        profile_form = self.profile_form_class
        context = {
            'profile': profile,
            'user_form': user_form(
                initial={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email}),
            'profile_form': profile_form(
                initial={
                    'default_full_name': full_name,
                    'default_phone_number': phone_number,
                    'default_address_line_1': address_line_1,
                    'default_address_line_2': address_line_2,
                    'default_town_or_city': town_or_city,
                    'default_county': county,
                    'default_postcode': postcode,
                    'default_country': country,
                    'dob': dob})
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Update the user's profile data.
        """
        user_form = self.user_form_class(
            data=request.POST, instance=request.user)
        profile_form = self.profile_form_class(
            data=request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your details has been successfully updated.')
        else:
            get_error_text = user_form.errors.as_text().split('*')[-1]
            messages.error(request, get_error_text)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Redirect back to the same page and display the updated data.
        """
        return reverse_lazy(
            'profile_detail', kwargs={
                'pk': self.request.user.pk})


class OrderHistoryView(View):
    """
    A view to display the specified user's order history.
    """
    template_name = 'profiles/order_history.html'

    def get(self, request, *args, **kwargs):
        """
        Retrieve all the orders from the specified user.
        """
        profile = get_object_or_404(Profile, user=request.user)
        orders = Order.objects.filter(profile=profile)
        context = {
            'orders': orders
        }
        return render(request, self.template_name, context)


class SingleOrderView(DetailView):
    """
    A view to display a single order summary.
    """
    model = Order
    template_name = 'checkout/checkout_success.html'

    def get_context_data(self, **kwargs):
        """
        Retrieve the specified order.
        """
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(
            order_number=self.kwargs['order_number'])
        context['past_order'] = True
        return context


class AddToWishlistView(LoginRequiredMixin, View):
    """
    A view to add a book to the user's wishlist.
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Add the specified book to the user's wishlist.
        If already exists, just give them feedback.
        """
        book = get_object_or_404(Book, id=pk)

        if Wishlist.objects.filter(user=request.user).exists():
            if Wishlist.objects.filter(user=request.user, books__id=pk):
                messages.info(request, f'{book} is already in your wishlist.')
            else:
                wishlist_obj = Wishlist.objects.get(user=request.user)
                wishlist_obj.books.add(book)
                messages.success(
                    request, f'{book} has been added to your wishlist.')
        else:
            object, created = Wishlist.objects.get_or_create(user=request.user)
            object.books.add(book)
            messages.success(
                request, f'{book} has been added to your wishlist.')

        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class WishlistDisplayView(LoginRequiredMixin, ListView):
    """
    A view to display the specified user's wishlist.
    """
    model = Wishlist
    template_name = 'books/books.html'
    paginate_by = 16
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
        Get a list of books in their wishlist.
        Allow the user to sort the books.
        """
        sort_option = self.get_sort_option()
        qs = Book.objects.filter(wishlist__user=self.request.user)
        if sort_option:
            qs = qs.order_by(sort_option)
        return qs

    def get_context_data(self, **kwargs):
        """
        Get a context and add extra information to use in the template.
        """
        context = super().get_context_data(**kwargs)

        if self.sort and self.sort[0] == '-':
            self.sort = self.sort[1:]

        if self.sort is not None:
            context['sort_params'] = (f'&sort={self.sort}&direction='
                                      f'{self.direction}')
        context['sort'] = self.sort
        context['direction'] = self.direction
        context['current_sorting'] = f'{self.sort}_{self.direction}'
        context['total'] = self.get_queryset().count()
        context['title'] = 'Wishlist'

        return context


class RemoveFromWishList(View):
    """
    A view to remove the specified book from the user's wishlist.
    """
    def post(self, request, pk, *args, **kwargs):
        """
        Remove the specified book from the user's wishlist.
        """
        book = get_object_or_404(Book, id=pk)
        wishlist = get_object_or_404(Wishlist, user=request.user)
        wishlist.books.remove(book)
        wishlist.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class ManagementView(UserPassesTestMixin, TemplateView):
    """
    A view displays account menu options.
    """
    template_name = 'profiles/management_menu.html'

    def test_func(self):
        """
        Check if the logged-in user is the superuser.
        """
        return self.request.user.is_superuser
