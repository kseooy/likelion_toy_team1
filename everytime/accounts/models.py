from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 닉네임 필드 (중복 비허용)
    nickname = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username}의 프로필 ({self.nickname})"