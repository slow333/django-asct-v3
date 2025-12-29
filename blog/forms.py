from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': '제목',
            'title_tag': '슬러그',
            'content': '내용',
            'category': '카테고리',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '제목을 입력하세요', 
                'style': 'margin-bottom: 10px;font-size:20px;'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control text-muted', 
                'placeholder': '내용을 입력하세요',
                'style': 'margin-bottom: 10px;'}),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'style': 'margin-bottom: 10px;'}),
        }
        
class PostFormAdmin(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','title_tag', 'content', 'author', 'category']
        labels = {
            'title': '제목',
            'title_tag': '슬러그',
            'content': '내용',
            'author': '작성자',
            'category': '카테고리',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '제목을 입력하세요', 
                'style': 'margin-bottom: 10px;font-size:20px;'}),
            'title_tag': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '태그를 입력하세요',
                'style': 'margin-bottom: 10px;'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': '내용을 입력하세요',
                'style': 'margin-bottom: 10px;'}),
            'author': forms.Select(attrs={
                'class': 'form-select',
                'style': 'margin-bottom: 10px;'}),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'style': 'margin-bottom: 10px;'}),
        }