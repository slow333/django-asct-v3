from django.urls import path
from . import views
from .models import Question, Choice
from .views import QuestionIndexView, QuestionDetailView, QuestionResultsView, QuestionVoteView,CreateQuestionView, QuestionUpdateView, QuestionDeleteView


# apps/polls/
app_name = "polls"

urlpatterns = [
    path("", QuestionIndexView.as_view(), name="index"),
    path("create/", CreateQuestionView.as_view(), name="create"),
    
    path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
    path("<int:pk>/update/",QuestionUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", QuestionDeleteView.as_view(), name="delete"),
    
    path("<int:pk>/results/", QuestionResultsView.as_view(), name="results"),
    path("<int:pk>/vote/", QuestionVoteView.as_view(), name="vote"),
]