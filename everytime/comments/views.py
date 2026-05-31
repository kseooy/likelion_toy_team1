from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Comment

@login_required
def comment_create(request, post_id):
    """댓글 및 대댓글 작성 기능"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)  # id 필드 매칭
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        is_anonymous = request.POST.get('is_anonymous') == 'on'  # 체크박스 선택 여부
        
        if content:
            comment = Comment(
                post=post,
                author=request.user,
                content=content,
                is_anonymous=is_anonymous
            )
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
    
    if request.user == comment.author:
        comment.delete()
        
    return redirect('posts:detail', id=post_id)


# ✨ 댓글 수정 기능 
@login_required
def comment_update(request, comment_id):
    """댓글 수정 기능"""
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id  # 수정 전/후에 돌아갈 원본 게시글 ID
    
    # 1. 작성자가 아니면 원래 게시글로 튕겨내기
    if request.user != comment.author:
        return redirect('posts:detail', id=post_id)
        
    # 2. [POST] 실제로 수정을 완료하고 수정 완료 버튼을 눌렀을 때
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
        return redirect('posts:detail', id=post_id)
        

    return redirect('posts:detail', id=post_id)


@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id # 좋아요 처리 후 다시 돌아갈 원래 게시글 ID
    
    # 이미 좋아요를 누른 유저라면 목록에서 제거 (좋아요 취소)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        # 처음 누르는 유저라면 목록에 추가 (좋아요)
        comment.like_users.add(request.user)
        
    # 원래 보고 있던 게시글 상세 페이지로 돌려보내기
    return redirect('posts:detail', id=post_id)