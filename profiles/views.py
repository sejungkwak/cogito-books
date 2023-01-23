from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProfileView(TemplateView, LoginRequiredMixin):
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
