from django.contrib import admin
from library.models import Author, Genre, Book, BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 1
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # list_filter = ('genre',)
    list_select_related = ('author',)
    list_per_page = 20
    inlines = [BooksInstanceInline]
    
    search_fields = ('title', 'author__last_name')
    
    # m2m field에 대하 추가 쿼리 방지(사전에 join을 수행)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('genre')

    def display_genre(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all()[:3])
    display_genre.short_description = 'Genre'

admin.site.register(Genre)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status',)
    list_select_related = ('book',)
    list_per_page = 20
    search_fields = ( 'borrower',)
    autocomplete_fields = ('borrower',)
    

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
