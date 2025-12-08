from django import forms
from .models import Post
from django.forms import ModelForm

class PostForm(ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['title', 'content']
