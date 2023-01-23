from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.ProfileView.as_view(),
         name='profile'),
    path('<int:pk>/account_detail/',
         views.ProfileUpdateView.as_view(),
         name='profile_detail'),
    path('<int:pk>/order_history/',
         views.OrderHistoryView.as_view(),
         name='order_history'),
    path('<int:pk>/order_history/<order_number>',
         views.SingleOrderView.as_view(),
         name='single_order_history'),
]
