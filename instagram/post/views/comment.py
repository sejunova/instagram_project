from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from ..forms import CommentForm
from ..models import Post, PostComment

__all__ = (
    'comment_create',
    'comment_delete',
)

def comment_create(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

        next_path = request.GET.get('next', '').strip()
        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post.pk)

def comment_delete(request, comment_pk):
    next_path = request.GET.get('next', '').strip()
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path:
                return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다')
