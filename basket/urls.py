from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('',
         TemplateView.as_view(template_name='basket/basket.html'),
         name='view_basket'),
    path('add/<int:pk>/',
         views.AddToBasketView.as_view(),
         name='add_to_basket'),
    path('edit/<int:pk>/',
         views.EditBasketView.as_view(),
         name='edit_basket'),
]
