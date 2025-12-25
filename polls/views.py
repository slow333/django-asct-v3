from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Question, Choice
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import generic
from django.forms import inlineformset_factory

class QuestionIndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'questions'
    paginate_by = 5
    ordering = ['-pub_date']

class QuestionDetailView(generic.DetailView):
    model = Question

ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), extra=3, can_delete=False)

class CreateQuestionView(generic.CreateView):
    model = Question
    fields = ['question_text', 'category']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['choice_formset'] = ChoiceFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context['choice_formset']
        if choice_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.pub_date = timezone.now()
            self.object.save()
            form.save_m2m()
            choice_formset.instance = self.object
            choice_formset.save()
            messages.success(self.request, '질문이 생성되었습니다.')
            return redirect(self.success_url) # type: ignore
        else:
            return self.render_to_response(self.get_context_data(form=form))


class QuestionUpdateView(generic.UpdateView):
    model = Question
    fields = ['question_text', 'category']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceFormSet(self.request.POST, instance=self.object)
        else:
            context['choice_formset'] = ChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context['choice_formset']
        if choice_formset.is_valid():
            self.object = form.save()
            choice_formset.instance = self.object
            choice_formset.save()
            messages.success(self.request, '질문이 수정되었습니다.')
            return redirect(self.success_url) # type: ignore
        else:
            return self.render_to_response(self.get_context_data(form=form))

class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')
    
    def form_valid(self, form):
        messages.success(self.request, '질문이 삭제되었습니다.')
        return super().form_valid(form) # type: ignore

class QuestionResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class QuestionVoteView(generic.View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice']) # type: ignore
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/question_detail.html', {
                'question': question,
                "error_message": "선택해야 합니다.",
            })
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            messages.success(request, f'투표가 완료되었습니다. {selected_choice.choice_text}를 투표했습니다.')
            return redirect('polls:results', question.pk)

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

def vote(request, pk):
    question = Question.objects.get(pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # type: ignore
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            "error_message": "선택해야 합니다.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        messages.success(request, f'투표가 완료되었습니다. {selected_choice.choice_text}를 투표했습니다.')
        return redirect('polls:results', question.id) # type: ignore
