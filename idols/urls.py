from django.urls import path
from . import views

# apps/idols/
urlpatterns = [
    path('', views.idol_home, name='idol-home'),
    path('upload/', views.upload, name='idol-upload'),
    path('<int:pk>/detail', views.detail, name='idol-detail'),
    path('<int:pk>/delete', views.delete, name='idol-delete'),
    path('<int:pk>/update', views.update, name='idol-update'),
]