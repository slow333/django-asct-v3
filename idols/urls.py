from django.urls import path
from . import views

# apps/idols/
app_name = 'idols'

urlpatterns = [
    path('', views.idol_home, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<int:pk>/detail', views.detail, name='detail'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('<int:pk>/update', views.update, name='update'),
]