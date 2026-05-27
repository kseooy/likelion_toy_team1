from django.contrib import admin
from .models import Professor, Post, PostImage

#admin.site.register(Post)
#admin.site.register(PostImage)

# Post 테이블을 관리자 페이지에서 예쁘게 보여주기 위한 설정
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'name']
    list_filter = ['department']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 목록에 보여줄 필드 (학과/교수명 대신 연결된 professor 객체를 띄움)
    list_display = ['id', 'professor', 'title', 'rating', 'views_count', 'created_at']
    # 클릭하면 상세 페이지로 들어갈 필드
    list_display_links = ['id', 'title']
    # 우측 필터 사이드바 (별점별 모아보기 가능)
    list_filter = ['rating']


# 이미지는 기본 방식으로 등록
admin.site.register(PostImage)