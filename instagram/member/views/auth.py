from django.contrib.auth import logout as django_logout, login as django_login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config.settings import FACEBOOK_APP_ID, FACEBOOK_SCOPE
from ..forms import SignUpForm, LoginForm

__all__=(
    'signup',
    'login',
    'logout',
)

def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            django_login(request, user)
            return redirect('post:post_list')
    signup_form = SignUpForm()
    context = {
        'signup_form': signup_form,
    }
    return render(request, 'member/signup.html', context)


def login(request):
    next_path = request.GET.get('next')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.login(request)
            if next_path:
                return redirect(next_path)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login credentials invalid')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,
        'facebook_app_id': FACEBOOK_APP_ID,
        'scope': ','.join(FACEBOOK_SCOPE),
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')
