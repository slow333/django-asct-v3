from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from aistore.forms import SearchForm
from users.models import Profile

def blog_home(request):
    # prefetch author and its one-to-one Profile to avoid extra queries in template
    post_list = Post.objects\
        .select_related('author', 'author__profile')\
        .order_by('author__username').all()
    
    # 검색 폼 처리
    search_form = SearchForm(request.GET or None)
    search_title = request.GET.get('search_title', '')
    
    if search_title:
        post_list = post_list.filter(title__icontains=search_title)

    paginator = Paginator(post_list, 8) # 한 페이지에 8개씩 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_title': search_title,
        'post_list': page_obj,
    }

    return render(request, 'blog/home.html', context)

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "새로운 글이 등록되었습니다.")
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})

@login_required
def blog_update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "글이 수정되었습니다.")
            return redirect('blog-home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/update.html', {'form': form})

@login_required
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/detail.html', {'post': post})

@login_required
def blog_user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')

    paginator = Paginator(posts, 4) # 한 페이지에 8개씩 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'username': user.username}
    
    return render(request, 'blog/user_posts.html', context)

@login_required
def blog_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        messages.success(request, "글이 삭제되었습니다.")
        post.delete()
        return redirect('blog-home')
    else:
        return render(request, 'blog/delete.html', {'post': post})



def index(request):
    return render(request, 'index.html')