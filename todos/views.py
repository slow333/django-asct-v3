from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Todo
from .forms import TodoForm
from calendar import HTMLCalendar
from datetime import datetime
import calendar

class TodoCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, todos=None):
        self.year = year
        self.month = month
        self.todos = todos
        super(TodoCalendar, self).__init__()

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday bg-light"></td>'
        
        events_html = ""
        if self.todos:
            day_todos = [t for t in self.todos if t.start_date and t.start_date.day == day]
            for t in day_todos:
                events_html += f'<div class="text-truncate"><a href="/apps/todos/detail/{t.id}/" class="badge bg-primary text-white" style="font-size: 0.7rem; display: block; margin-bottom: 2px; {t.is_completed and 'text-decoration: line-through;' or 'text-decoration: none;'}">{t.title[:10]}...</a></div>'
        
        return f'<td class="{self.cssclasses[weekday]} border" style="height: 100px; vertical-align: top; width: 14.28%;"><div class="fw-bold mb-1">{day}</div>{events_html}</td>'

    def formatmonth(self, withyear=True):
        v = super().formatmonth(self.year, self.month, withyear) # type: ignore
        return v.replace('<table border="0" cellpadding="0" cellspacing="0" class="month">', '<table class="table table-bordered text-start">')

def index(request, year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month

    # Calendar setup
    todos_list = Todo.objects.filter(start_date__year=year, start_date__month=month)
    cal = TodoCalendar(year, month, todos_list).formatmonth(withyear=True)
    
    paginator = Paginator(todos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Previous/Next Month Calculation
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1

    month_name = list(calendar.month_name)[month]
    time = datetime.now().strftime('%I:%M:%S %p')
    todos = Todo.objects.all().order_by('start_date')
    context = {'cal': cal, 'year': year, 'month': month, 
            'time': time, 'month_name': month_name,
            'page_obj': page_obj, 'today': datetime.today(),
            'prev_year': prev_year, 'prev_month': prev_month,
            'next_year': next_year, 'next_month': next_month,
    }
    return render(request, 'todos/index.html', context )
    
def todo_list(request):
    queryset = Todo.objects.all().order_by('start_date')
    
    search_query = request.GET.get('searched')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)
    
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'todos/todo-list.html', {'page_obj': page_obj})

def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    return render(request, 'todos/create.html', {'form': form})

def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id) 
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos:detail', todo_id=todo.id) # type: ignore
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/update.html', {'form': form, 'todo': todo,})

def delete(request, todo_id):
    if request.method == 'POST':
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return redirect('todos:index')
    else:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return redirect('todos:index')

def detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    return render(request, 'todos/detail.html', {'todo': todo})
