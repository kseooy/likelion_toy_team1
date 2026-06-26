from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # 필수 항목 누락이나 글자 수 제한 알림창(messages) 기능
from django.contrib.auth.decorators import login_required  # 로그인 권한 데코레이터 추가
from .models import Professor, Post, PostImage
from django.db.models import Q
from django.http import JsonResponse
from comments.models import Comment
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    return redirect('accounts:login')


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


@login_required
def create(request):
    """
    2. 교수 후기 작성 화면
    - [수정 완료] 익명 선택 해제 시 실명(user) 작성 가능하도록 로직 보완
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
        
        # 💡 명시적 삼항 연산자로 수정: 체크박스 해제 시 확실하게 False 지정
        is_anonymous = True if request.POST.get('is_anonymous') == 'on' else False
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

        # 💡 user=request.user 를 추가하여 작성자가 정확히 매칭되도록 수정했습니다.
        post = Post.objects.create(
            professor=selected_professor,
            rating=int(rating),
            title=title,
            content=content,
            user=request.user,
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
    - 추가: related_name='comments'를 반영한 실시간 에타식 익명 시스템
    """
    post = get_object_or_404(Post, id=id)
    
    # [조회수 증가 로직]
    post.views_count += 1
    post.save()

    # ------------------ [에타식 익명 번호 계산 로직] ------------------
    comments = post.comments.all().order_by('created_at')
    
    anonymous_dict = {}
    anonymous_count = 1
    
    post_author_id = post.user.id if post.user else None

    for comment in comments:
        if comment.is_anonymous:  # 익명 체크가 된 댓글/대댓글인 경우
            if comment.author and comment.author.id == post_author_id:
                comment.anonymous_name = "익명(글쓴이)"
            elif comment.author and comment.author.id in anonymous_dict:
                comment.anonymous_name = f"익명{anonymous_dict[comment.author.id]}"
            else:
                if comment.author:
                    anonymous_dict[comment.author.id] = anonymous_count
                comment.anonymous_name = f"익명{anonymous_count}"
                anonymous_count += 1
        else:
            # 실명 댓글인 경우
            comment.anonymous_name = comment.author.username if comment.author else "알 수 없음"
    # ------------------------------------------------------------------

    context = {
        'post': post,
        'comments': comments,  
    } 

    return render(request, 'posts/detail.html', context)


@login_required
def update(request, id):
    """
    4. 게시글 수정하기 (Professor 모델 외래키 구조 이식)
    - [보안 보완] 타인이 URL 주소 조작으로 강제 접근할 경우 차단하는 로직 추가
    """
    post = get_object_or_404(Post, id=id)
    
    # 💡 [보안 장치] 타인이 수정을 시도하면 글 상세페이지로 튕겨내기
    if post.user != request.user:
        messages.error(request, "본인이 작성한 글만 수정할 수 있습니다.")
        return redirect('posts:detail', id=post.id)
    
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
        
        # 💡 명시적 삼항 연산자로 수정: 체크박스 해제 시 확실하게 False 지정
        is_anonymous = True if request.POST.get('is_anonymous') == 'on' else False
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


@login_required
def delete(request, id):
    """
    5. 게시글 삭제하기
    - [보안 보완] 타인이 URL 주소 조작으로 강제 접근할 경우 차단하는 로직 추가
    """
    post = get_object_or_404(Post, id=id)
    
    # 💡 [보안 장치] 타인이 삭제를 시도하면 글 상세페이지로 튕겨내기
    if post.user != request.user:
        messages.error(request, "본인이 작성한 글만 삭제할 수 있습니다.")
        return redirect('posts:detail', id=post.id)
        
    for img in post.images.all():
        img.image.delete() 
    post.delete()
    
    return redirect('posts:list')


@login_required
def post_like(request, post_id):
    """
    6. 게시글 좋아요 누르기 기능
    """
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:
        # Django 내장 메시지 기능 활용함!
        messages.error(request, "본인의 글에는 좋아요를 누를 수 없습니다.")
        return redirect('posts:detail', id=post.id)

    # 좋아요
    if post.like_users.filter(id=request.user.id).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)

    return redirect('posts:detail', id=post.id)


@login_required
def post_bookmark(request, post_id):
    """
    7. 게시글 북마크(저장) 토글 기능 - 에타 보관함의 '북마크' 탭에 사용!
    """
    post = get_object_or_404(Post, id=post_id)

    # 북마크(저장)는 내 글도 저장할 수 있는 게 일반적이므로 본인 차단 로직은 생략했습니다!
    
    # 이미 북마크를 누른 상태라면 취소(제거)
    if post.bookmark_users.filter(id=request.user.id).exists():
        post.bookmark_users.remove(request.user)
    else:
        # 누르지 않았다면 북마크 목록에 추가
        post.bookmark_users.add(request.user)

    # 처리가 끝나면 다시 보던 상세 페이지로 복귀
    return redirect('posts:detail', id=post.id)


def search(request):
    """
    8. 검색 전용 페이지 및 검색 결과 반환 
    - 최근 검색어 저장(최대 5개, 최신순)
    - 많이 찾는 교수 리스트 전달
    """
    search_query = request.GET.get('q', '').strip() # 공백 제거 추가
    posts = []
    
    # 💡 세션에서 현재 유저의 최근 검색어 목록 가져오기 (없으면 빈 리스트)
    search_history = request.session.get('search_history', [])

    if search_query:
        # 최근 검색어 목록 갱신 및 최신순 정렬
        if search_query in search_history:
            search_history.remove(search_query) # 기존에 있던 같은 단어는 지우고
        search_history.insert(0, search_query) # 맨 앞에 추가
        
        # 최근 검색어는 최대 5개까지만 유지
        search_history = search_history[:5]
        request.session['search_history'] = search_history
        request.session.modified = True # 세션 변경 사항을 DB/쿠키에 강제 저장
        
        posts = Post.objects.filter(
            Q(title__icontains=search_query) |          
            Q(content__icontains=search_query) |        
            Q(professor__name__icontains=search_query)  
        ).order_by('-id') 
        
    context = {
        'posts': posts,
        'search_query': search_query, 
        'search_history': search_history, # HTML 화면에 최근 검색어 목록 전달
        'popular_professors': ["김교수", "이교수", "박교수"], # 많이 찾는 교수 탑3 (우선 임시 하드코딩)
    }
    return render(request, 'posts/search.html', context)


@csrf_exempt
def clear_search_history(request):
    """
    9. 최근 검색어 전체 삭제 API (프론트엔드 비동기 JavaScript 요청용)
    """
    if request.method == "POST":
        if 'search_history' in request.session:
            del request.session['search_history']
            request.session.modified = True
        return JsonResponse({"result": "success", "message": "최근 검색어가 전체 삭제되었습니다."})
    return JsonResponse({"result": "fail", "message": "잘못된 요청입니다."}, status=400)



@login_required
def archive(request):
    """
    10. 보관함 기능 (내가 좋아요 한 후기 / 내가 저장(북마크)한 후기 목록 조회)
    """
    # 좋아요 한 글
    liked_posts = request.user.like_posts.all().order_by('-id')
    # 북마크 한 글
    bookmarked_posts = request.user.bookmark_posts.all().order_by('-id')

    # 몇 개인지 카운트
    liked_count = liked_posts.count()
    bookmarked_count = bookmarked_posts.count()

    context = {
        'liked_posts': liked_posts,
        'bookmarked_posts': bookmarked_posts,
        'liked_count': liked_count,
        'bookmarked_count': bookmarked_count,
    }
    return render(request, 'posts/archive.html', context)



