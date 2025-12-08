from aistore.models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'unit_price', 'inventory', 'collection', 'description']

class SearchForm(forms.Form):
    search_title = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2 p-1',
            'style': 'width:90%;',
            'placeholder': '제목으로 검색...',
        })
    )