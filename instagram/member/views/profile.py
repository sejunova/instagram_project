from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

__all__ = (
    'profile',
)


def profile(request, nickname):
    profile_user = User.objects.get(nickname=nickname)
    posts = profile_user.posts.all()
    context = {
        'profile_user': profile_user,
        'posts': posts,
    }
    return render(request, 'member/profile.html', context)