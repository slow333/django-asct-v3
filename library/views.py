from django.db.models import Count
from django.shortcuts import render
from django.views import generic
from library.models import Book, BookInstance, Author
from django.core.paginator import Paginator

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'library/index.html', context=context)

def book_list(request):
    queryset = Book.objects.all().select_related('author')
    author_id = request.GET.get('author_id')
    if author_id:
        queryset = queryset.filter(author__id=author_id)
        
    search_query = request.GET.get('searched','')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)
        
    paginator = Paginator(queryset, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    book_count = Book.objects.count()
    context = {
        'page_obj': page_obj,
        'book_count': book_count,
    }
    
    return render(request, 'library/book_list.html', context)

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

def author_list(request):
    queryset = Author.objects.annotate(book_count=Count('book'))
    
    paginator = Paginator(queryset, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'library/author_list.html', context)

def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    author_books = Book.objects.filter(author=author)
    context = {
        'author': author,
        'author_books': author_books,
    }
    return render(request, 'library/author_detail.html', context)

def book_instances(request):
    queryset = BookInstance.objects.all().select_related('book')
    
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    book_instances = paginator.get_page(page)
    
    context = {
        'page_obj': book_instances,
    }
    
    return render(request, 'library/bookinstance_list.html', context)

def book_instance_detail(request, pk):
    book_instance = BookInstance.objects.get(pk=pk)
    book_status = list(BookInstance.LOAN_STATUS)
    context = {
        'bookinstance': book_instance,
        'book_status': book_status,
    }
    return render(request, 'library/bookinstance_detail.html', context)

def book_instance_status_change(request, pk):
    book_instance = BookInstance.objects.get(pk=pk)
    book_instance.status = request.POST.get('book_instance_status')
    book_instance.save()
    return book_instance_detail(request, pk)

def book_instance_available(request):
    book_instance = BookInstance.objects.filter(status__exact='a').select_related('book')
    paginator = Paginator(book_instance, 20)
    page = request.GET.get('page')
    book_instances = paginator.get_page(page)
    
    context = {
        'bookinstance_list': book_instances,
    }
    
    return render(request, 'library/bookinstance_list.html', context)
