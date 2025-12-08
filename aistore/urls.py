from django.urls import path
from . import views

# /apps/aistore/
urlpatterns = [
    path('', views.home, name='aistore-home'),
    path('create/', views.product_create, name='product-create'),
    path('bulk-action/', views.product_bulk_action, name='product-bulk-action'),
]
