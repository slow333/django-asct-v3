from django.forms import ModelForm
from .models import Idol
from django import forms
from crispy_forms.helper import FormHelper

class IdolForm(ModelForm):
    class Meta:
        model = Idol
        fields = ['title','image', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class IdolTitleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False # 폼의 모든 레이블을 숨깁니다.
    class Meta:
        model = Idol
        fields = ['title']