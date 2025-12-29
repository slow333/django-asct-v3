from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.db.models import Q, Count
from .models import Post
from .forms import PostForm, PostFormAdmin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # 앱이름/템플릿이름.html
    # default context: object_list, post_list(paginated_by적용됨)
    # paginate_by가 적용되면 자동으로 page_obj라는 컨텍스트 변수가 추가됨
    # 수동으로 정의 => context_object_name = 'posts' 
    ordering = ['-updated_at']
    paginate_by = 5 

    def get_queryset(self):
        # select_related를 사용하여 author와 author의 profile을 미리 로드(join)합니다.
        queryset = super().get_queryset()\
            .select_related('author')\
            .select_related('author__profile')
        search_title = self.request.GET.get('searched', '')
        if search_title:
            queryset = queryset.filter(Q(title__contains=search_title) | Q(author__username__icontains=search_title))
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset
    
    # GetContextData를 오버라이드하여 context에 추가 정보 전달 가능
    # 이거 이해가 안됨. 모르겠음............
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 카테고리별 게시글 수 집계
        categories = Post.objects.values('category').annotate(count=Count('id'))
        print(categories)
        
        # 카테고리 코드를 디스플레이 이름으로 변환 (choices가 있는 경우)
        category_field = Post._meta.get_field('category')
        choices = dict(category_field.choices) # type: ignore
        print(choices)
        
        context['categories'] = categories
        context['choices'] = choices
        
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    # default context: object, post

    # 디테일 화면으로 이동하기 이전 페이지 URL을 세션에 저장
    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        if referer and request.path not in referer:
            request.session['previous_url'] = referer
        return super().get(request, *args, **kwargs)

# form을 사용하여 게시글 생성
# add, update, delete시에 기본으로 model의 get_absolute_url()을 호출하여 이동
# 이를 오버라이드하여 다른 url로 이동할 수도 있음(예: success_url 속성 사용)
class PostAddFormView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    
    def get_form_class(self):
        if self.request.user.is_superuser:
            return PostFormAdmin
        return PostForm

    def form_valid(self, form):
        if 'author' not in form.cleaned_data:
            form.instance.author = self.request.user
        messages.success(self.request, '새 게시글이 생성되었습니다.')
        return super().form_valid(form)

class PostAddView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'content', 'author']
    
    labels = {
        'title': '제목',
        'content': '내용',
        'author': '작성자',
    }
    # 내가 생성한 form 커스터마이징
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields:
            form.fields[field].widget.attrs.update({
                'class': 'form-control', 
                'style': 'margin-bottom: 10px;', 
                'placeholder': f'{self.labels.get(field, "")}을 입력하세요'})
            form.fields[field].label = self.labels.get(field, "")
        form.fields['author'].widget.attrs.update({'class': 'form-select'})
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '새 게시글이 생성되었습니다.')
        return super().form_valid(form)

class PostUpdateFormView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update.html'
    
    def get_form_class(self):
        if self.request.user.is_superuser:
            return PostFormAdmin
        return PostForm

    def form_valid(self, form):
        messages.success(self.request, '게시글이 수정되었습니다.')
        return super().form_valid(form)

# 삭제하기 이전 리스트 페이지를 기억했다가 삭제하면 그 페이지로 돌아감
# 삭제가 detail 페이지에서만 가능한 점을 이용
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog:index')
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        referer = request.META.get('HTTP_REFERER')
        if referer and request.path not in referer:
            if self.object.get_absolute_url() not in referer: # type: ignore
                request.session['previous_url'] = referer
        return response

    def get_success_url(self) -> str:
        previous_url = self.request.session.pop('previous_url', None)
        if previous_url:
            return previous_url
        return reverse_lazy('blog:index')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    paginate_by = 4
    ordering = ['-updated_at']
    
    # GetContextData를 오버라이드하여 context에 추가 정보 전달 가능
    # 여기서는 username을 이용하여 info_message를 추가
    # queryset을 추가해서 새로운 값을 넣어 줄수도 있음
    def get_context_data(self, **kwargs):
        username = self.kwargs.get('username')
        kwargs['info_message'] = mark_safe(f'<span>{username} 님의 게시글 목록입니다.</span>')
        filtered_count = Post.objects.filter(author__username=username).count()
        kwargs['filtered_count'] = filtered_count
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        # select_related를 사용하여 author와 author의 profile을 미리 로드(join)합니다.
        queryset = super().get_queryset().select_related('author').select_related('author__profile')
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = queryset.filter(author=user).order_by('-updated_at')
        messages.success(self.request, f'{user.username} 님의 게시글 입니다.')
        return queryset