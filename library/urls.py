from django.urls import path
from . import views

# /app/library/
app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('bookinstances/', views.BookInstanceListView.as_view(), name='bookinstances'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(), name='bookinstance-detail'),
    path('bookinstance_available/', views.BookInstanceAvailableListView.as_view(), name='bookinstance-available'),
]