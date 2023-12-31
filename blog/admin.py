from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'blog_date')
    search_fields = ['title', 'comment']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Blog, BlogAdmin)
