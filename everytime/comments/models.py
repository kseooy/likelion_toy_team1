from django.db import models
from django.contrib.auth.models import User
from posts.models import Post  # 친구가 만든 진짜 Post 모델 임포트

class Comment(models.Model):
    # Post 모델과 N:1 관계 설정
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # 댓글 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 대댓글 구현을 위한 자기참조 외래키 (대댓글이 아니면 null)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # 에브리타임 속성
    is_anonymous = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_comments')

    class Meta:
        ordering = ['created_at']  # 기본적으로 작성된 시간 순서대로 정렬

    def __str__(self):
        return f"{'대댓글: ' if self.parent else '댓글: '}{self.content[:10]}"

    @property
    def like_count(self):
        return self.likes.count()