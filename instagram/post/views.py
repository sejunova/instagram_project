from django.shortcuts import render

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
