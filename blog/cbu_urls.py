from django.urls import path # type: ignore
from . import cbv_views

# apps/blog/
app_name = 'blog'

urlpatterns = [
    path('', cbv_views.PostListView.as_view(), name='index'),
    path('add/', cbv_views.PostAddFormView.as_view(), name='add'),
    path('<int:pk>/update', cbv_views.PostUpdateFormView.as_view(), name='update'),
    path('<int:pk>/delete', cbv_views.PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail', cbv_views.PostDetailView.as_view(), name='detail'),
    path('<str:username>/user-posts', cbv_views.UserPostListView.as_view(), name='user-posts'),
    path('<int:pk>/like', cbv_views.PostLikeView.as_view(), name='like-post'),
    path('<int:pk>/add-comment', cbv_views.AddCommentView.as_view(), name='add-comment'),
    path('<int:pk>/delete-comment', cbv_views.DeleteCommentView.as_view(), name='delete-comment'),
    path('<int:pk>/edit-comment', cbv_views.EditCommentView.as_view(), name='edit-comment'),
]
