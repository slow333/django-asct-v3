from django.contrib import admin
from django.utils.html import format_html
from .models import Idol

@admin.register(Idol)
class IdolAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'thumbnail_image']
    search_fields = ['title']
    readonly_fields = ['created_at']
    
    def thumbnail_image(self, Idol):
        if Idol.thumbnail:
            return format_html(f'<img src="{Idol.thumbnail.url}" width="40" />')
        return "No Image"