# posts/migrations/0010_merge_fix.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # 배포 서버에서 충돌을 일으킨 두 명의 주범을 적어줍니다.
        ('posts', '0009_alter_post_user'),
    ]

    operations = [
        # 빈 파일이므로 데이터베이스를 건드리지 않고 연결고리 역할만 한다
    ]