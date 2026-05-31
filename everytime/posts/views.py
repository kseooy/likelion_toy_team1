from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # 필수 항목 누락이나 글자 수 제한 알림창(messages) 기능
from .models import Professor, Post, PostImage
from django.db.models import Q

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
    departments = Professor.objects.values_list('department', flat=True).distinct().order_by('department')
    
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
    4. 게시글 수정하기 (Professor 모델 외래키 구조 이식)
    """
    post = get_object_or_404(Post, id=id)
    
    # 수정을 위해 학과 선택창 목록을 가져옴 (ㄱㄴㄷ순)
    departments = Professor.objects.values_list('department', flat=True).distinct().order_by('department')
    
    # 수정 화면 진입 시 기존에 등록되어 있던 교수의 학과를 기본값으로 세팅
    selected_dept = request.GET.get('department', post.professor.department)
    professors = Professor.objects.filter(department=selected_dept).order_by('name')
    
    if request.method == "POST":
        professor_id = request.POST.get('professor_id')
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        new_images = request.FILES.getlist('images')

        # [예외처리 1] 필수 항목 빈값 검증
        if not (professor_id and rating and title and content):
            messages.error(request, "필수 항목을 모두 입력해주세요.")
            return render(request, 'posts/update.html', {'post': post, 'departments': departments, 'selected_dept': selected_dept, 'professors': professors})

        # [예외처리 2] 본문 1000자 제한 검증
        if len(content) > 1000:
            messages.error(request, "본문은 1000자 이하로 작성해주세요.")
            return render(request, 'posts/update.html', {'post': post, 'departments': departments, 'selected_dept': selected_dept, 'professors': professors})

        # [예외처리 3] 새로 올린 이미지 개수가 5장을 초과하는지 검증
        if len(new_images) > 5:
            messages.error(request, "이미지는 최대 5장까지만 첨부할 수 있습니다.")
            return render(request, 'posts/update.html', {'post': post, 'departments': departments, 'selected_dept': selected_dept, 'professors': professors})

        # 외래키 구조로 덮어쓰기 진행
        selected_professor = get_object_or_404(Professor, id=professor_id)
        post.professor = selected_professor
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
        
    return render(request, 'posts/update.html', {
        'post': post,
        'departments': departments,
        'selected_dept': selected_dept,
        'professors': professors
    })

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



def post_like(request, post_id):

    print("좋아요 함수 실행됨")

    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
        
    # ❌ 기존: return redirect('posts:detail', post_id=post.id)
    # ✨ 변경: 친구의 URL 규칙에 맞춰 post_id 대신 id로 변경!
    return redirect('posts:detail', id=post.id)


def search(request):
    """
    7. 검색 전용 페이지 및 검색 결과 반환
    - 검색창에 처음 들어왔을 때는 빈 화면을 보여주고
    - 검색어를 입력하고 엔터를 치면 그에 맞는 게시글 목록을 필터링하여 리턴함
    """
    search_query = request.GET.get('q', '') # 프론트엔드 검색창의 name="q" 값을 가져옴
    posts = []
    
    # 사용자가 검색어를 입력하고 검색을 요청했을 때만 DB를 조회
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) |          # 제목에 검색어가 포함되거나
            Q(content__icontains=search_query) |        # 본문에 검색어가 포함되거나
            Q(professor__name__icontains=search_query)  # 우리가 주입한 교수님 이름에 포함된 경우
        ).order_by('-id') # 최신순 정렬
        
    context = {
        'posts': posts,
        'search_query': search_query, # 내가 뭘 검색했는지 창에 남겨주기 위한 변수
    }
    return render(request, 'posts/search.html', context) # 프론트에서 만든 검색 전용 HTML로 렌더링