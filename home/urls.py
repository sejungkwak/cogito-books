from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('',
         views.BookListView.as_view(),
         name='home'),
    path('privacy_policy/',
         TemplateView.as_view(
             template_name='home/privacy_policy.html'),
         name='privacy_policy'),
    path('terms_and_conditions/',
         TemplateView.as_view(
             template_name='home/terms_conditions.html'),
         name='terms_conditions'),
    path('about_us/',
         TemplateView.as_view(
             template_name='home/about.html'),
         name='about_us'),
    path('faq/',
         TemplateView.as_view(
            template_name='home/faq.html'),
         name='faq'),
]
