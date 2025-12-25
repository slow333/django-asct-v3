from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue, MyClubUser
from .forms import VenueForm, EventForm

def index(request, year=datetime.now().year, month=datetime.now().month):
    cal = HTMLCalendar().formatmonth(year, month)
    return render(request, 'events/index.html', 
        { 'cal': cal, 'year': year, 'month': month, })

def venues_list(request):
    venues = Venue.objects.all().order_by('-name')
    
    pagenator = Paginator(venues, 10)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    
    return render(request, 'events/venues_list.html', {'page_obj': page_obj, })

def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '새로운 장소가 생성되었습니다')
            return redirect('events:venues-list')
    else:
        form = VenueForm()
        return render(request, 'events/venue_create.html', {'form': form })

def venue_search(request):
    if request.method == 'POST':
        searched = request.POST['venue_search']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/venue_search.html', 
                    {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/venue_search.html')

def venue_details(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/venue_details.html', {'venue': venue})

def venue_update(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('events:venues-list')
    return render(request, 'events/venue_update.html', {'venue': venue, 'form': form})

def venue_delete(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if request.method == 'POST':
        venue.delete()
        return redirect('events:venues-list')

def events_list(request):
    events = Event.objects.all().order_by('-event_date')
    pagenator = Paginator(events, 10)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    return render(request, 'events/events_list.html',{'page_obj': page_obj,})

def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events:events-list')
    return render(request, 'events/event_create.html', {'form': form})

def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_details.html', {'event': event})

def event_update(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events:events-list')
    return render(request, 'events/event_update.html', {'event': event, 'form': form})

def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events:events-list')

def event_search(request):
    if request.method == 'POST':
        searched = request.POST['event_search']
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/event_search.html', {'searched': searched, 'events': events})
    else:
        return render(request, 'events/event_search.html', {})

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})