from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin, VenueFormAdmin
import calendar
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def index(request, year=datetime.now().year, month=datetime.now().month):
    cal = HTMLCalendar().formatmonth(year, month)
    month_name = list(calendar.month_name)[month]
    time = datetime.now().strftime('%I:%M:%S %p')
    return render(request, 'events/index.html', 
        { 'cal': cal, 'year': year, 'month': month, 
        'time': time, 'month_name': month_name,})

def venues_list(request):
    venues = Venue.objects.all().order_by('name')
    search_venue = request.GET.get('searched', '')
    
    if search_venue:
        venues = venues.filter(name__icontains=search_venue)
    
    pagenator = Paginator(venues, 10)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    
    return render(request, 'events/venues_list.html', {'page_obj': page_obj, })

def venue_create(request):
    if not request.user.is_authenticated:
        messages.success(request, "장소를 생성하려면 로그인이 필요합니다.")
        return redirect('login')
    if request.method == 'POST':
        if request.user.is_superuser:
            form = VenueFormAdmin(request.POST, request.FILES or None,)
        else:
            form = VenueForm(request.POST, request.FILES or None,)
        if form.is_valid():
            venue = form.save(commit=False)
            if not request.user.is_superuser:
                venue.owner = request.user.id
            venue.save()
            messages.success(request, '새로운 장소가 생성되었습니다')
            return redirect('events:venue-details', venue_id=venue.id)
    else:
        if request.user.is_superuser:
            form = VenueFormAdmin()
        else:
            form = VenueForm()
        return render(request, 'events/venue_create.html', {'form': form })

def venue_details(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    try:
        owner_name = User.objects.get(pk=venue.owner)
    except User.DoesNotExist:
        owner_name = "지정한 소유자가 없습니다."
    return render(request, 'events/venue_details.html', {'venue': venue, 'owner_name': owner_name })

def venue_update(request, venue_id):
    if not request.user.is_authenticated:
        messages.success(request, "장소를 수정하려면 로그인이 필요합니다.")
        return redirect('login')
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('events:venues-list')
    return render(request, 'events/venue_update.html', {'venue': venue, 'form': form})

def venue_delete(request, venue_id):
    if not request.user.is_authenticated:
        messages.success(request, "장소를 삭제하려면 로그인이 필요합니다.")
        return redirect('login')
    venue = Venue.objects.get(pk=venue_id)
    if request.method == 'POST':
        venue.delete()
        return redirect('events:venues-list')

def events_list(request):
    events = Event.objects.all().order_by('-event_date')
    search_event = request.GET.get('searched', '')
    
    if search_event:
        events = events.filter(name__icontains=search_event)
    
    pagenator = Paginator(events, 10)
    page = request.GET.get('page')
    page_obj = pagenator.get_page(page)
    return render(request, 'events/events_list.html',{'page_obj': page_obj,})

def event_create_venue(request, venue_id):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 생성하려면 로그인이 필요합니다.")
        return redirect('login')
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST or None)
            if form.is_valid():
                event = form.save(commit=False)
                if venue_id:
                    venue = get_object_or_404(Venue, pk=venue_id)
                    event.venue = venue
                event.save()
                messages.info(request, "이벤트가 생성되었습니다.")
                return redirect('events:events-list')
        else:
            form = EventForm(request.POST or None)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                if venue_id:
                    venue = get_object_or_404(Venue, pk=venue_id)
                    event.venue = venue
                event.save()
                messages.info(request, "이벤트가 생성되었습니다.")
                return redirect('events:events-list')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
    return render(request, 'events/event_create.html', {'form': form })

def event_create(request):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 생성하려면 로그인이 필요합니다.")
        return redirect('login')
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST or None)
            if form.is_valid():
                form.save()
                messages.info(request, "이벤트가 생성되었습니다.")
                return redirect('events:events-list')
        else:
            form = EventForm(request.POST or None)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                messages.info(request, "이벤트가 생성되었습니다.")
                return redirect('events:events-list')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
    return render(request, 'events/event_create.html', {'form': form })

def event_details(request, event_id):
    
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_details.html', {'event': event})

def event_update(request, event_id):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 수정하려면 로그인이 필요합니다.")
        return redirect('login')
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events:events-list')
    return render(request, 'events/event_update.html', {'event': event, 'form': form})

def event_delete(request, event_id):
    if not request.user.is_authenticated:
        messages.success(request, "이벤트를 삭제하려면 로그인이 필요합니다.")
        return redirect('login')
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events:events-list')

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})