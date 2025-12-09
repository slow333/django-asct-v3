from django.contrib import admin
from django.utils.html import format_html
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_filter = ['user__username']
    list_display = ['user__username', 'image_preview']
    search_fields = ['user__username',]
    list_select_related = ['user',]
    list_per_page = 20
    list_select_related = ['user']
    ordering = ('user__username',)
    
    # def user_username(self, profile):
    #     return profile.user.username
    # user_username.admin_order_field = 'user__username'
    # user_username.short_description = 'Username'

    def image_preview(self, profile):
        if profile.image:
            return format_html('<img src="{}" style="width: 30px; height: auto;" />', profile.image.url)
        return "No Image"
    image_preview.short_description = 'Profile Image'