from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .models import Profile
from .forms import UserUpdateForm, ProfileForm


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
    Edit a user's own details and default delivery address.
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
                    'full_name': full_name,
                    'phone_number': phone_number,
                    'address_line_1': address_line_1,
                    'address_line_2': address_line_2,
                    'town_or_city': town_or_city,
                    'county': county,
                    'postcode': postcode,
                    'country': country,
                    'dob': dob})
        }
        return render(request, self.template_name, context)
