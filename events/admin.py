from django.contrib import admin
from events.models import Event, Venue, MyClubUser


admin.site.site_header = "Events 관리자 페이지" # H1 헤더 및 로그인 양식 상단 텍스트
admin.site.site_title = "Events" # 브라우저 페이지 <title> 태그 접미사
admin.site.index_title = "Event 관리자 대시보드에 오신 것을 환영합니다" 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ('manager','attendees')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
    list_select_related = ('venue','manager')
    search_fields = ('manager','name', 'event_date')


class EventInline(admin.StackedInline):
    model = Event
    extra = 3
    autocomplete_fields = ['manager']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')
    inlines = [EventInline]


@admin.register(MyClubUser)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    ordering = ('last_name',)
    search_fields = ('last_name','first_name', 'email')
