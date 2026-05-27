from django.contrib import admin
from .models import Post, PostImage

#admin.site.register(Post)
#admin.site.register(PostImage)

# Post 테이블을 관리자 페이지에서 예쁘게 보여주기 위한 설정
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 관리자 페이지 목록에 보여줄 필드들
    list_display = ['id', 'department', 'professor_name', 'title', 'rating', 'created_at']
    # 클릭하면 상세 페이지로 들어갈 필드들
    list_display_links = ['id', 'title']
    # 우측에 필터 사이드바 추가 (학과별, 별점별로 모아보기 가능)
    list_filter = ['department', 'rating']

# PostImage는 기본 방식으로 등록
admin.site.register(PostImage)