from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from member.decorators import login_required
from ..forms import PostForm, CommentForm
from ..models import Post

__all__ = (
    'post_list',
    'post_create',
    'post_detail',
    'post_delete',
    'post_like_toggle',
)

def post_list(request):
    """모든 포스트목록 리턴,
    템프릿은 'post/post_list.html'을 사용
    """
    # posts = Post.objects.exclude(author=None)
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('member:login')

    # Form 사용 할 때!
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        # GET 요청인 경우, 빈 PostForm인스턴스를 생성해서 탬플릿에 전달
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    # post = get_object_or_404(Post.objects.exclude(author=None), pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied


@login_required
def post_like_toggle(request, post_pk):
    if not request.user.is_authenticated:
        return render(request, 'member:login')
    next_path = request.GET.get('next')
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user

        filtered_like_posts = user.like_posts.filter(pk=post_pk)
        if filtered_like_posts.exists():
            user.like_posts.remove(post)
        else:
            user.like_posts.add(post)
        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post_pk)
