from django.forms import ModelForm, DateTimeInput
from .models import Venue, Event

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'zip_code', 'phone', 'web', 'email_address']
        labels = {
            'name': '장소이름',
            'address': '주소',
            'zip_code': '우편번호',
            'phone': '전화번호',
            'web': '웹사이트',
            'email_address': '이메일 주소',
        }

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'manager', 'attendees', 'description']
        labels = {
            'name': '집회 이름',
            'event_date': '날짜',
            'venue': '장소',
            'manager': '관리자',
            'attendees': '참석자',
            'description': '설명',
        }
        widgets = {
            'event_date': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})