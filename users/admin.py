from django.contrib import admin
from django.utils.html import format_html
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_username', 'image_preview']
    search_fields = ['user_username',]
    list_select_related = ['user',]

    def user_username(self, profile):
        return profile.user.username

    def image_preview(self, profile):
        if profile.image:
            return format_html('<img src="{}" style="width: 30px; height: auto;" />', profile.image.url)
        return "No Image"
    image_preview.short_description = 'Profile Image'