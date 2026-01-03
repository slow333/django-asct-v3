from django.urls import path # type: ignore
from . import fbv_views

# apps/blog/
app_name = 'blog'

urlpatterns = [
    path('', fbv_views.post_list, name='index'),
    path('add/', fbv_views.add_post, name='add'),
    path('<int:pk>/update', fbv_views.update_post, name='update'),
    path('<int:pk>/delete', fbv_views.delete_post, name='delete'),
    path('<int:pk>/detail', fbv_views.post_detail, name='detail'),
    path('<str:username>/user-posts', fbv_views.user_post_list, name='user-posts'),
    path('<int:pk>/like', fbv_views.like_post, name='like-post'), # type: ignore
    path('<int:pk>/add-comment', fbv_views.add_comment, name='add-comment'),
    path('<int:pk>/delete-comment', fbv_views.delete_comment, name='delete-comment'),
    path('<int:pk>/edit-comment', fbv_views.edit_comment, name='edit-comment'),
]
