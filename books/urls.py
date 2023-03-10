from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.BookListView.as_view(),
         name='book_list'),
    path('<int:pk>/',
         views.BookDetailView.as_view(),
         name='book_detail'),
    path('add_book/',
         views.BookCreateView.as_view(),
         name='add_book'),
    path('edit_book/<int:pk>/',
         views.BookUpdateView.as_view(),
         name='edit_book'),
    path('delete_book/<int:pk>/',
         views.BookDeleteView.as_view(),
         name='delete_book'),
    path('<int:pk>/reviews/',
         views.ReviewListView.as_view(),
         name='review_list'),
    path('<int:book_id>/edit_review/<int:pk>/',
         views.ReviewUpdateView.as_view(),
         name='edit_review'),
    path('<int:book_id>/delete_review/<int:pk>/',
         views.ReviewDeleteView.as_view(),
         name='delete_review'),
    path('add_author/',
         views.AuthorCreateView.as_view(),
         name='add_author'),
    path('add_book_of_the_month/',
         views.RecommendationCreateView.as_view(),
         name='add_book_of_the_month'),
    path('book_of_the_month/<int:pk>/',
         views.RecommendationDetailView.as_view(),
         name='book_of_the_month'),
    path('book_of_the_month/<int:pk>/edit/',
         views.RecommendationUpdateView.as_view(),
         name='edit_book_of_the_month'),
    path('book_of_the_month/<int:pk>/delete/',
         views.RecommendationDeleteView.as_view(),
         name='delete_book_of_the_month')
]
