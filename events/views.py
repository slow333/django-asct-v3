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
from django.http import HttpResponse
import csv
import codecs
# PDF generation imports(py -m pip install reportlab 명령어로 설치 필요)
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def venue_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    textobject = p.beginText()
    textobject.setTextOrigin(inch, inch)
    
    # 한글 폰트 등록 (Windows: malgun.ttf, Mac: AppleGothic.ttf 등)
    try:
        pdfmetrics.registerFont(TTFont('Malgun', 'malgun.ttf'))
        font_name = 'Malgun'
    except:
        font_name = 'Helvetica' # 폰트 파일이 없을 경우 기본 폰트 사용
    textobject.setFont(font_name, 15)

    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(f"Name: {venue.name}")
        lines.append(f"Address: {venue.address}")
        lines.append(f"Zip Code: {venue.zip_code}")
        lines.append(f"Phone: {venue.phone}")
        lines.append(f"Web: {venue.web}")
        lines.append(f"Email Address: {venue.email_address}")
        lines.append(" ")

    for line in lines:
        textobject.textLine(line)
        # 페이지 넘김 처리
        if textobject.getY() > letter[1] - inch:
            p.drawText(textobject)
            p.showPage()
            textobject = p.beginText()
            textobject.setTextOrigin(inch, inch)
            textobject.setFont(font_name, 15)

    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='venues.pdf')

def venue_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    # 한글 깨짐 방지
    response.write(codecs.BOM_UTF8)
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Zip Code', 'Phone', 'Web', 'Email Address'])
    
    venues = Venue.objects.all().order_by('name')
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    
    return response

def venue_text(request):
    url_name = request.resolver_match
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venue_text.txt"'
    
    venues =Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(f"{venue.name}\n")
        lines.append(f"{venue.address}\n")
        lines.append(f"{venue.zip_code}\n")
        lines.append(f"{venue.phone}\n")
        lines.append(f"{venue.web}\n")
        lines.append(f"{venue.email_address}\n")
        lines.append("\n")
    response.writelines(lines)
    return response

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