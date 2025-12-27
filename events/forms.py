from django import forms
from django.utils.safestring import mark_safe
from .models import Venue, Event, MyClubUser
from django.contrib.auth.models import User

class VenueFormAdmin(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'owner', 'venue_image']
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'owner': mark_safe('<span style="display: inline-block; font-size: 1rem; margin: 10px;">Owner id(User.id)</span>'),
            'email_address': '',
            'venue_image': '',
        }
    def __init__(self, *args, **kwargs):
        super(VenueFormAdmin, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'placeholder': f'{field.replace("_", " ").capitalize()}'})

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_image']
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '장소 이름' }),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '주소' }),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '우편번호' }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호' }),
            'web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': '웹사이트' }),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일 주소' }),
        }

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
class VenueChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.event_set.count()})" # type: ignore


class EventFormAdmin(forms.ModelForm):
    venue = VenueChoiceField(
        queryset=Venue.objects.all().order_by('name'), 
        required=False, 
        label='', 
        empty_label='장소 선택',
        widget=forms.Select(attrs={
            'class': 'form-select', 'placeholder': '장소 선택'}))
    manager = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'), 
        required=False, 
        label='',
        empty_label='관리자 선택',
        widget=forms.Select(attrs={'class': 'form-select'}))
    attendees = forms.ModelMultipleChoiceField(
        queryset=MyClubUser.objects.all().order_by('-first_name'), 
        required=False, 
        label =mark_safe('<span style="display: inline-block; font-size: 1rem; margin: 10px; color:red;">참석자</span>'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        )

    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'manager', 'attendees', 'description']
        labels = {
            'name': '',
            'event_date': '',
            'manager': '',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '집회 이름' }),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '설명'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventFormAdmin, self).__init__(*args, **kwargs)
        if self.fields['attendees']:
            self.fields['attendees'].label_suffix = ''

class EventForm(forms.ModelForm):
    venue = VenueChoiceField(
        queryset=Venue.objects.all().order_by('name'), 
        required=False, 
        label='', 
        empty_label='장소 선택',
        widget=forms.Select(attrs={
            'class': 'form-select', 'placeholder': '장소 선택'}))
    attendees = forms.ModelMultipleChoiceField(
        queryset=MyClubUser.objects.all().order_by('-first_name'), 
        required=False, 
        label =mark_safe('<span style="display: inline-block; font-size: 1rem; margin: 10px; color:red;">참석자</span>'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'attendees', 'description']
        labels = {
            'name': '',
            'event_date': '',
            'venue': '',
            'attendees': '참석자',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '집회 이름' }),
            'event_date': forms.DateTimeInput(attrs={
                'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '설명'}),
        }
