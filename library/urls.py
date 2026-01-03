from django.urls import path
from . import views

# /app/library/
app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='books'),
    path('authors/', views.author_list, name='authors'),
    path('bookinstances/', views.book_instances, name='bookinstances'),
    path('book/<int:pk>', views.book_detail, name='book-detail'),
    path('author/<int:pk>', views.author_detail, name='author-detail'),
    path('bookinstance/<uuid:pk>', views.book_instance_detail, name='bookinstance-detail'),
    path('bookinstance_available/', views.book_instance_available, name='bookinstance-available'),
    path('book_instance_status_change/<uuid:pk>', views.book_instance_status_change, name='book_instance_status_change'),
    
    
]