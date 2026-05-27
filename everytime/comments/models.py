from django.db import models
from django.contrib.auth.models import User
from posts.models import Post  

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    # 로그인 없이 테스트용
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_anonymous = models.BooleanField(default=True)

    like_users = models.ManyToManyField(User, related_name='like_comments', blank=True)

    class Meta:
        ordering = ['created_at']  

    def __str__(self):
        return f"{'대댓글: ' if self.parent else '댓글: '}{self.content[:10]}"

    @property
    def like_count(self):
        return self.like_users.count()