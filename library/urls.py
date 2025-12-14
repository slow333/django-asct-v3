from django.urls import path
from . import views

# /app/library/
urlpatterns = [
    path('', views.index, name='library-home'),
    path('books/', views.BookListView.as_view(), name='library-books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='library-authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),


]