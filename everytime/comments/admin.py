from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'short_content', 'parent', 'is_anonymous', 'created_at']
    list_filter = ['is_anonymous', 'created_at']
    search_fields = ['content', 'author__username']

    def short_content(self, obj):
        return obj.content[:20]
    short_content.short_description = '댓글 내용 요약'