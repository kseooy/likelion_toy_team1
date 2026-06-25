from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Comment
from django.contrib import messages  
from django.urls import reverse 

@login_required
def comment_create(request, post_id):
    """댓글 및 대댓글 작성 기능"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)  
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        is_anonymous = request.POST.get('is_anonymous') == 'on'  
        
        if content:
            # 모델의 필드명(author, is_anonymous)과 정확히 매칭됩니다.
            comment = Comment(
                post=post,
                author=request.user,  
                content=content,
                is_anonymous=is_anonymous
            )
            # 대댓글일 경우 parent_id가 외래키 ID로 저장됩니다.
            if parent_id:
                comment.parent_id = int(parent_id)
            comment.save()
            
        return redirect('posts:detail', id=post.id)
        
    return redirect('posts:list')


# ✨ 댓글 삭제 기능
@login_required
def comment_delete(request, comment_id):
    """댓글 및 대댓글 삭제 기능"""
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    
    # 모델의 작성자 필드명인 comment.author와 정확히 일치합니다.
    if request.user == comment.author:
        comment.delete()
        
    return redirect('posts:detail', id=post_id)


# ✨ 댓글 수정 기능 
@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    
    # 모델의 작성자 필드명인 comment.author와 정확히 일치합니다.
    if request.user != comment.author:
        return redirect('posts:detail', id=post_id)
        
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
        return redirect('posts:detail', id=post_id)
        
    return render(request, 'comment_update.html', {'comment': comment})


@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id 
    
    # 1. 본인 글 차단
    if comment.author == request.user:
        # 📍 주소창 뒤에 직접 에러 파라미터를 붙여서 보냅니다.
        return redirect(f'/detail/{post_id}/?error=mine')
    
    # 2. 좋아요 토글 로직
    is_liked = comment.like_users.filter(pk=request.user.pk).exists()
    
    if is_liked:
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
        
    return redirect('posts:detail', id=post_id)