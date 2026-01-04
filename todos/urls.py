from django.urls import path

from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.index, name='index'),
    path('list/', views.todo_list, name='list'),
    path('create/', views.create, name='create'),
    path('update/<int:todo_id>/', views.update, name='update'),
    path('delete/<int:todo_id>/', views.delete, name='delete'),
    path('detail/<int:todo_id>/', views.detail, name='detail'),
]
