from django.urls import path # type: ignore
from . import views

# apps/blog/
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('add/', views.PostAddFormView.as_view(), name='add'),
    path('<int:pk>/update', views.PostUpdateFormView.as_view(), name='update'),
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail', views.PostDetailView.as_view(), name='detail'),
    path('<str:username>/user-posts', views.UserPostListView.as_view(), name='user-posts'),
    path('<int:pk>/like', views.PostLikeView.as_view(), name='like-post'),
    path('<int:pk>/add-comment', views.AddCommentView.as_view(), name='add-comment'),
    path('<int:pk>/delete-comment', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('<int:pk>/edit-comment', views.EditCommentView.as_view(), name='edit-comment'),
]
