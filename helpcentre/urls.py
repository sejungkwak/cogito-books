from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('contact_us/',
         views.contact_us,
         name='contact_us'),
    path('faq/',
         TemplateView.as_view(
            template_name='helpcentre/faq.html'),
         name='faq'),
]
