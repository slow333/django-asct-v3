from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Count
from django.shortcuts import render
from django.views import generic
from library.models import Book, BookInstance, Author

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
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

class BookListView(generic.ListView):
    model = Book
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author')
        author_id = self.request.GET.get('author_id')
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        return queryset
    # template에 너어줄 list 이름(default: book_list)
    context_object_name = 'books' 
    # template으로 사용할 파일 지정(default: app_name/book_list.html)
    template_name = 'library/book_list.html'
    # 임의의 context 값을 넣어 주는 방법
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        # context에 필요한 값을 정의해서 넣어줌
        context['book_count'] = Book.objects.count()
        return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 20
    
    # book은 author model에 자동생성됨
    def get_queryset(self):
        return Author.objects.annotate(author_book_count=Count('book'))
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
    # 저자의 책목록을 찾는 context를 생성
    def get_context_data(self, **kwargs):
        # 기본 컨텍스트(author 객체)를 가져옵니다.
        context = super().get_context_data(**kwargs)
        # 저자의 책 목록을 컨텍스트에 추가합니다.
        context['author_books'] = Book.objects.filter(author=self.object) # type: ignore
        return context

class BookInstanceListView(generic.ListView):
    model = BookInstance
    paginate_by = 20
    
class BookInstanceDetailView(generic.DetailView):
    model = BookInstance

class BookInstanceAvailableListView(generic.ListView):
    model = BookInstance
    paginate_by = 20
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='a').select_related('book')