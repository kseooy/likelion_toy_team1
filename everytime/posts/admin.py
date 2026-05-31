from django.contrib import admin
from .models import Post, PostImage

# admin.site.register(Post)
# admin.site.register(PostImage)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'rating', 'created_at']
    
    list_display_links = ['id', 'title']
    
    list_filter = ['rating']

# PostImage는 기본 방식으로 등록
admin.site.register(PostImage)