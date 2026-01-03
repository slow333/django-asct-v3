from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Todo
from .forms import TodoForm
from calendar import HTMLCalendar
from datetime import datetime
import calendar

def index(request, year=datetime.now().year, month=datetime.now().month):
    cal = HTMLCalendar().formatmonth(year, month)
    month_name = list(calendar.month_name)[month]
    time = datetime.now().strftime('%I:%M:%S %p')
    return render(request, 'todos/index.html', 
        { 'cal': cal, 'year': year, 'month': month, 
        'time': time, 'month_name': month_name,})
    
def todo_list(request):
    todos = Todo.objects.all().order_by('start_date')
    
    paginator = Paginator(todos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'todos/home.html', {'page_obj': page_obj})

def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'todos/create.html', {'form': form, 'success': True})
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
    return render(request, 'todos/update.html', {'form': form})

def delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return render(request, 'todos/delete.html', {'todo': todo})

def detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    return render(request, 'todos/detail.html', {'todo': todo})
