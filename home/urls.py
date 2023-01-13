from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('',
        TemplateView.as_view(
            template_name='home/index.html'),
        name='home'),
    path('privacy_policy/',
        TemplateView.as_view(
            template_name='home/privacy_policy.html'),
        name='privacy_policy'),
    path('terms_and_conditions/',
        TemplateView.as_view(
            template_name='home/terms_conditions.html'),
        name='terms_conditions'),
]
