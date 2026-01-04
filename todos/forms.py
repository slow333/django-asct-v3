from django.forms import ModelForm
from django import forms
from .models import Todo

class TodoForm(ModelForm):
    class Meta:        
        model = Todo
        fields = ('title', 'content', 'start_date', 'end_date', 'is_completed', 'user')
        
        labels = {
            'title': '',
            'content': '',
            'start_date': '시작일',
            'end_date': '종료일',
            'is_completed': '완료여부 ',
            'user': '작성자',
        }
        
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 5}),
            'start_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_completed': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'style': 'margin-left: 10px;font-size: 1.2rem;'}),
            'user': forms.Select(
                attrs={'class': 'form-select'}),
        }
