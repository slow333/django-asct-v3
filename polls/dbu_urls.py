from django.urls import path
from . import views
from .views import QuestionDetailView, QuestionResultsView, QuestionVoteView,CreateQuestionView, QuestionUpdateView, QuestionDeleteView

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", CreateQuestionView.as_view(), name="create"),
    
    path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
    path("<int:pk>/update/",QuestionUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", QuestionDeleteView.as_view(), name="delete"),
    
    path("<int:pk>/results/", QuestionResultsView.as_view(), name="results"),
    path("<int:pk>/vote/", QuestionVoteView.as_view(), name="vote"),
]