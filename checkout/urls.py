from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.CheckoutView.as_view(),
        name='checkout'),
    path(
        'checkout_success/<uuid:order_number>',
        views.CheckoutSuccessView.as_view(),
        name='checkout_success'),
]
