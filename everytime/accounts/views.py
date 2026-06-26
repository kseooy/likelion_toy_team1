from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# 로그인
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) 
            return redirect('posts:list')
        else:
            messages.error(request, "아이디 또는 비밀번호가 틀렸습니다.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# 로그아웃
def logout_view(request):
    auth_logout(request) 
    return redirect('accounts:login')


# 회원가입 
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # 자동 로그인(auth_login) 제거! 비밀번호 암호화 후 DB 저장만 수행
            return redirect('accounts:signup_complete') 
        else:
            messages.error(request, "회원가입 정보가 올바르지 않습니다. 다시 확인해주세요.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


# 회원가입 완료 창 뷰 (완료 창 + 로그인 하러 가기 버튼 대응)
def signup_complete(request):
    return render(request, 'accounts/signup_complete.html')


# 아이디 중복 확인 API (프론트엔드 비동기 JavaScript 요청용)
@csrf_exempt
def check_username(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username", "")
            
            # 아이디 4~12자
            if len(username) < 4 or len(username) > 12:
                return JsonResponse({"result": "fail", "message": "아이디는 4~12자여야 합니다."}, status=400)
                
            if User.objects.filter(username=username).exists():
                return JsonResponse({"result": "fail", "message": "이미 사용 중인 아이디입니다."}, status=200)
                
            return JsonResponse({"result": "success", "message": "사용 가능한 아이디입니다."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"result": "fail", "message": "잘못된 요청 데이터입니다."}, status=400)