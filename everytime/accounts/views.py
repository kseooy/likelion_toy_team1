# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

def login_view(request):
    """
    1. 로그인 로직 (장고 내장 인증 폼 사용)
    """
    if request.method == "POST":
        # 사용자가 화면 폼에 입력한 아이디/비밀번호를 검증
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) 
            return redirect('posts:list') # 로그인 성공 시 메인 게시판으로 이동
        else:
            messages.error(request, "아이디 또는 비밀번호가 틀렸습니다.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    2. 로그아웃 로직
    """
    auth_logout(request) 
    return redirect('accounts:login') # 로그아웃 시 메인 게시판으로 이동