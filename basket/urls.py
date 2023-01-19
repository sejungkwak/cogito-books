from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('',
         TemplateView.as_view(template_name='basket/basket.html'),
         name='view_basket'),
]
