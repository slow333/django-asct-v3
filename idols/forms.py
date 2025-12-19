from django.forms import ModelForm
from .models import Idol
from django import forms
from crispy_forms.helper import FormHelper

class IdolForm(ModelForm):
    title = forms.CharField(max_length=100)
    image = forms.ImageField()
    thumbnail = forms.ImageField(required=False)
    class Meta:
        model = Idol
        fields = ['title','image', 'thumbnail']
        

class IdolTitleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False # 폼의 모든 레이블을 숨깁니다.
    class Meta:
        model = Idol
        fields = ['title']