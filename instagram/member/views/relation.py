from django.contrib.auth import get_user_model
from django.shortcuts import render

from member.decorators import login_required

User = get_user_model()

__all__ = (
    'follow',
)


@login_required
def follow(request, nickname):
    user = request.user
    profile_user = User.objects.get(nickname=nickname)
    posts = profile_user.posts.all()
    user.follow_toggle(user=profile_user)
    context = {
        'user': user,
        'profile_user': profile_user,
        'posts': posts,
    }
    return render(request, 'member/profile.html', context)
