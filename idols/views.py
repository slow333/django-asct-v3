from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import IdolForm, IdolTitleForm
from .models import Idol

def index(request):
    idol_list = Idol.objects.order_by('title').all()
    search_title = request.GET.get('searched', '')
    
    if search_title:
        idol_list = idol_list.filter(title__icontains=search_title)

    paginator = Paginator(idol_list, 8) # 한 페이지에 8개씩 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'idol/idol-home.html', context)

def upload(request):
    if request.method == 'POST':
        form = IdolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('idols:index')
    else:
        form = IdolForm()
    return render(request, 'idol/upload.html', {'form': form})

def update(request, pk):
    idol = Idol.objects.get(pk=pk)
    if request.method == 'POST':
        form = IdolForm(request.POST, request.FILES, instance=idol)
        if form.is_valid():
            form.save()
            messages.success(request, "글이 수정되었습니다.")
            return redirect('idols:detail', pk=idol.pk)
    else:
        form = IdolForm(instance=idol)
    return render(request, 'idol/update.html', {'form': form, 'idol': idol})

def detail(request, pk):
    idol = Idol.objects.get(pk=pk)
    if request.method == 'POST':
        form = IdolTitleForm(request.POST, instance=idol)
        if form.is_valid():
            form.save()
            return redirect('idols:detail', pk=idol.pk) # 수정 후 상세 페이지로 다시 리디렉션
    form = IdolTitleForm(instance=idol)
    return render(request, 'idol/detail.html', {'idol': idol, 'form': form})

def delete(request, pk):
    if request.method == 'POST':
        image = Idol.objects.get(pk=pk)
        image.delete()
        return redirect('idols:index')
    image = Idol.objects.get(pk=pk)
    return render(request, 'idol/delete.html', {'image': image})

def edit_title(request, pk):
    if request.method == 'POST':
        form = request.form.get('title')
        if form.is_valid():
            idol = Idol.objects.get(pk=pk)
            idol.title = form.cleaned_data['title']
            form.save()
            return redirect('idols:index')
    return render(request, 'idol/upload.html', {'form': form})     
        