from django.contrib import admin
from .models import News


@admin.register(News)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','status')
    list_filter = ('status', 'created', 'updated', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'updated'
    ordering = ('status', 'updated')