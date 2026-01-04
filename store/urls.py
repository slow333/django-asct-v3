from django.urls import path
from . import views

# /apps/store/
app_name = 'store'

urlpatterns = [
    path('', views.home, name='index'),
    path('create/', views.product_create, name='product-create'),
    path('edit/<int:product_id>/', views.product_edit, name='product-edit'),
    path('detail/<int:product_id>/', views.product_detail, name='product-detail'),
    path('bulk-action/', views.product_bulk_action, name='product-bulk-action'),
]
