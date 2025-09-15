from django.contrib import admin
from .models import BlogArticle


class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ('youtube_title', 'user', 'created_at')
    search_fields = ('youtube_title', 'generated_content')
    list_filter = ('created_at', 'user')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(BlogArticle, BlogArticleAdmin)