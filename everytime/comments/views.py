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

@login_required
def comment_like(request, comment_id):
    """댓글 좋아요 기능"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
        
    # 좋아요 클릭 후 다시 보던 게시글 상세 페이지로 리다이렉트
    return redirect('posts:detail', id=comment.post.id)

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
    
    if request.user != comment.author:
        return redirect('posts:detail', id=comment.post.id)
        
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
        return redirect('posts:detail', id=comment.post.id)
        
    return render(request, 'comment_update.html', {'comment': comment})