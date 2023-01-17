from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.BookListView.as_view(),
         name='book_list'),
    path('add_book/',
         views.BookCreateView.as_view(),
         name='add_book'),
    path('edit_book/<int:pk>',
         views.BookUpdateView.as_view(),
         name='edit_book')
]
