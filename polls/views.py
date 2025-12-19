from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Question
from django.contrib import messages
from django.core.paginator import Paginator

def index(request):
    question_list = Question.objects.order_by('-pub_date')
    
    paginator = Paginator(question_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question })


def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    choice = question.choice_set.get(pk=request.POST['choice']) # type: ignore
    choice.votes += 1
    choice.save()
    messages.success(request, f'투표가 완료되었습니다. {choice.choice_text}를 투표했습니다.')
    return redirect('polls:results', question_id=question.id) # type: ignore
