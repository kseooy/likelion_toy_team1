from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4
from django.utils import timezone

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d") 
    file_basename = os.path.basename(filename) 
    model_name = instance._meta.model_name
    return f'{model_name}/{today_str}/{str(uuid4())}_{file_basename}' 

class Professor(models.Model):
    department = models.CharField(max_length=100)  # 교수의 소속 학과 (필수)
    name = models.CharField(max_length=50)        # 교수명 (필수)

    def __str__(self):
        return f"[{self.department}] {self.name} 교수"


class Post(models.Model):
    # 나중 로그인 연동을 위해 임시로 null=True, blank=True를 주면 로그인 없이도 테스트가 수월해진다고 한다~~~
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()                        # 별점 (1~5, 필수)
    
    # 게시글 내용
    title = models.CharField(max_length=50)               # 제목 (필수) 
    content = models.TextField()                          # 본문 (필수) 
    
    # 선택 및 자동 생성 항목
    is_anonymous = models.BooleanField(default=True)       # 익명 여부 (선택)
    views_count = models.IntegerField(default=0)           # 조회수
    created_at = models.DateTimeField(auto_now_add=True)   # 작성일자 

    def __str__(self):
        return f"[{self.professor.department} - {self.professor.name} 교수님] {self.title}"
    

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_filepath)