from store.models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'unit_price', 'inventory', 'collection', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'inventory': forms.NumberInput(attrs={'class': 'form-control'}),
            'collection': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    searched = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '검색...',
            'style': 'width: 100%;',
            'aria-label': '검색'
        })
    )