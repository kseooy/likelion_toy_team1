# accounts/urls.py
from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),   # 로그인
    path('logout/', logout_view, name='logout'), # 로그아웃
    path('signup/',signup, name='signup'),
]