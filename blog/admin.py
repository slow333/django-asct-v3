from django.contrib import admin
from .models import Post, Category, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ['title', 'author', 'date_posted']

admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('post', 'author')
    list_display = ('post', 'author', 'date_posted', 'content')
    list_filter = ('author__username', 'date_posted')
    search_fields = ('author__username', 'post__title')
    ordering = ('-date_posted',)