from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # 게시글 id를 받아서 댓글을 생성하는 경로
    path('create/<int:post_id>/', views.comment_create, name='comment_create'),
    # 댓글 고유 id를 받아서 좋아요를 처리하는 경로
    path('like/<int:comment_id>/', views.comment_like, name='comment_like'),
]