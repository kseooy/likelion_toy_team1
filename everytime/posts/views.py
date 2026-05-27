from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # 필수 항목 누락이나 글자 수 제한 알림창(messages) 기능
from .models import Professor, Post, PostImage

def list(request):
    """
    1. 교수 후기 메인페이지 (전체보기 목록 조회)
    - 최신순, 인기순 정렬 기능 포함
    """
    sort_by = request.GET.get('sort', 'latest') 
    
    if sort_by == 'popular':
        # 인기순: 조회수(views_count)가 많은 순서대로 정렬하여 쿼리셋을 가져옴
        posts = Post.objects.all().order_by('-views_count', '-id') 
    else:
        # 최신순: 기본값으로 가장 최근에 생성된 글(id 내림차순)부터 정렬함
        posts = Post.objects.all().order_by('-id') 
        
    return render(request, 'posts/list.html', {'posts': posts})


def create(request):
    """
    2. 교수 후기 작성 화면
    """
    departments = Professor.objects.values_list('department', flat=True).distinct()
    
    # 임시 변수 세팅
    selected_dept = request.GET.get('department', '') 
    professors = []
    
    if selected_dept:
        professors = Professor.objects.filter(department=selected_dept).order_by('name')

    if request.method == "POST":
        professor_id = request.POST.get('professor_id')
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        images = request.FILES.getlist('images')

        # [예외처리] 최종 교수가 선택되었는지 검증
        if not (professor_id and rating and title and content):
            messages.error(request, "학과와 교수님을 포함한 필수 항목을 모두 입력해주세요.")
            return render(request, 'posts/create.html', {
                'departments': departments,
                'selected_dept': selected_dept,
                'professors': professors
            })

        # 글자 수 1000자 제한, 이미지 제한 규칙 
        if len(content) > 1000:
            messages.error(request, "본문은 1000자 이하로 작성해주세요.")
            return render(request, 'posts/create.html', {'departments': departments, 'selected_dept': selected_dept, 'professors': professors})

        # 검증 통과 시 객체 안전 생성
        selected_professor = get_object_or_404(Professor, id=professor_id)

        post = Post.objects.create(
            professor=selected_professor,
            rating=int(rating),
            title=title,
            content=content,
            is_anonymous=is_anonymous
        )
        
        for img in images:
            PostImage.objects.create(post=post, image=img)
            
        return redirect('posts:list') 
        
    # 처음에 글 쓰기 화면에 진입했을 때 (GET)
    return render(request, 'posts/create.html', {
        'departments': departments,      # 1번 창에 뜰 학과 리스트
        'selected_dept': selected_dept,  # 사용자가 고른 학과 기억용
        'professors': professors         # 2번 창에 뜰 필터링된 교수 리스트
    })


def detail(request, id):
    """
    3. 게시글 상세보기 화면
    - 학과, 교수이름, 별점, 제목, 본문 전체, 첨부 이미지 n장 표시
    - 조건: 상세 페이지에 들어올 때마다 해당 데이터의 조회수가 +1 증가해야 함
    """
    post = get_object_or_404(Post, id=id)
    
    # [조회수 증가 로직] 게시글을 성공적으로 가져왔다면, DB에 저장하기 전에 조회수를 1 올림
    post.views_count += 1
    post.save() # 변경된 조회수를 데이터베이스에 최종 저장합니다.

    return render(request, 'posts/detail.html', {'post': post}) 



def update(request, id):
    """
    4. 게시글 수정하기 
    - GET: 기존 게시글 데이터를 포함한 수정 폼 표시
    - POST: 제출된 데이터로 유효성 검사 후 기존 데이터 덮어쓰기 및 이미지 교체 
    """
    post = get_object_or_404(Post, id=id)
    
    # 사용자가 수정하기 버튼(제출)을 눌렀을 때 (POST 요청)
    if request.method == "POST":
        # 사용자가 수정 폼에 새로 입력한 데이터 추출
        department = request.POST.get('department')
        professor_name = request.POST.get('professor_name')
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        new_images = request.FILES.getlist('images')

        # [예외처리 1] 필수 항목 빈값 검증
        if not (department and professor_name and rating and title and content):
            messages.error(request, "필수 항목을 모두 입력해주세요.")
            return render(request, 'posts/update.html', {'post': post})

        # [예외처리 2] 본문 1000자 제한 검증
        if len(content) > 1000:
            messages.error(request, "본문은 1000자 이하로 작성해주세요.")
            return render(request, 'posts/update.html', {'post': post})

        # [예외처리 3] 새로 올린 이미지 개수가 5장을 초과하는지 검증
        if len(new_images) > 5:
            messages.error(request, "이미지는 최대 5장까지만 첨부할 수 있습니다.")
            return render(request, 'posts/update.html', {'post': post})

        # 데이터 업데이트 및 덮어쓰기 
        post.department = department
        post.professor_name = professor_name
        post.rating = int(rating)
        post.title = title
        post.content = content
        post.is_anonymous = is_anonymous
        post.save() 

        if new_images:
            for old_img in post.images.all():
                old_img.image.delete() 
                old_img.delete()                   

            for img in new_images:
                PostImage.objects.create(post=post, image=img)

        return redirect('posts:detail', id=post.id)
    return render(request, 'posts/update.html', {'post': post})


def delete(request, id):
    """
    5. 게시글 삭제하기
    - 사용자가 요청한 id의 게시글을 찾아 데이터베이스에서 영구 삭제
    - 삭제 완료 후 메인 게시판 목록(list) 화면으로 사용자를 리다이렉트
    """
    post = get_object_or_404(Post, id=id)
    for img in post.images.all():
        img.image.delete() 
    post.delete()
    
    return redirect('posts:list')

# posts/views.py

def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
        
    # ❌ 기존: return redirect('posts:detail', post_id=post.id)
    # ✨ 변경: 친구의 URL 규칙에 맞춰 post_id 대신 id로 변경!
    return redirect('posts:detail', id=post.id)