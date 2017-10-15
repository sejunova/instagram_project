from django.http import HttpResponse
from django.shortcuts import render, redirect

from post.forms import ImageUploadForm
from post.models import Post


def post_list(request):
    """모든 포스트목록 리턴,
    템프릿은 'post/post_list.html'을 사용
    """
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(photo=form.cleaned_data['image'])
            return redirect('post_list')
    return HttpResponse('allowed only via POST')


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.postcomment_set.all()
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post/post_detail.html', context)
