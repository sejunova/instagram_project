from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from member.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, PostComment


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




    # Form 사용 안할 때!!!!!!!
    # photo = request.FILES.get('photo') #get을 사용하면 조건판별까지 가능!!
    # if request.method == 'POST' and request.FILES.get('photo'):
    #     # request.FILES를 통해서 파일을 가져온다. html의 form tag 안쪽에 enctype="multipart/form-data"를 추가해야
    #     # 이렇게 받아짐
    #     post = Post.objects.create(photo=photo)
    #     return HttpResponse(f'<img src="{post.photo.url}">')
    # elif request.method == 'GET':
    #     return render(request, 'post/post_create.html')
    #
    # return render(request, 'post/post_create.html')


def post_detail(request, post_pk):
    # post = get_object_or_404(Post.objects.exclude(author=None), pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


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
            # comment = PostComment.objects.create(post=post,
            #                                      content=form.cleaned_data['content'],
            #                                      author=request.user)

        next_path = request.GET.get('next', '').strip()
        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post.pk)

        # 이 부분은 이제 필요없다!!!
        # else:
        #     form = CommentForm()
        # context = {
        #     'form':form,
        # }
        # return render(request, 'post/comment_create.html', context)

def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied

def comment_delete(request, comment_pk):
    next_path = request.GET.get('next', '').strip()
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk = comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path:
                return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다')

@login_required
def post_like_toggle(request, post_pk):
    if request.method == 'POST':
        # if not request.user.is_authenticated:
        #     return redirect('member:login')
        next_path = request.GET.get('next')

        post = get_object_or_404(Post, pk=post_pk)
        user = request.user
        filtered_like_posts = user.like_posts.filter(pk=post.pk)
        if filtered_like_posts.exists():
            user.like_posts.remove(post)
        else:
            user.like_posts.add(post)

        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post_pk)




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




















