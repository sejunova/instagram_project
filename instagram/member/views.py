import json
from pprint import pprint
from typing import NamedTuple


from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login
import requests
from django.urls import reverse

from config.settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET_CODE, FACEBOOK_SCOPE
from member.decorators import login_required
from .forms import SignUpForm, LoginForm

User = get_user_model()  # User가 어디서 온건지 명확히 알 수 있다..?


def signup_old(request):  # forms.py 안쓰고 할 때
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            if User.objects.filter(username=username).exists():
                return HttpResponse(f' Username {username} already exists.')
            user = User.objects.create_user(username=username, password=password)
            return HttpResponse(f'{user.username}, {user.password}')
    return render(request, 'member/signup.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            # username = member_form.cleaned_data['username']
            # password = password=member_form.cleaned_data['password']
            # # 아래 과정은 이제 없어도 된다. 왜? forms.py에 클래스안에 검증메소드 추가함.
            # # if User.objects.filter(username=username).exists():
            # #     return HttpResponse(f' Username {username} already exists.')
            # user = User.objects.create_user(
            #     username=username,
            #     password=password,
            # )
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

def profile(request, nickname):
    profile_user = User.objects.get(nickname=nickname)
    posts = profile_user.posts.all()
    context = {
        'profile_user':profile_user,
        'posts':posts,
    }
    return render(request, 'member/profile.html', context)


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id =data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = FACEBOOK_APP_ID
    app_secret_code = FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET.get('code')

    def get_access_token_info(code_param): #code변수는 동적으로 받는다.
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login')
        )
        params_access_token = {'client_id': app_id, 'client_secret': app_secret_code,
                  'redirect_uri': redirect_uri, 'code': code_param}
        response = requests.get('https://graph.facebook.com/v2.10/oauth/access_token', params=params_access_token)
        return AccessTokenInfo(**response.json())

    token_info = get_access_token_info(code)
    access_token = token_info.access_token

    def get_debug_token_info(access_token_param):
        checked_params = {'input_token':access_token_param, 'access_token':app_access_token}
        response = requests.get('https://graph.facebook.com/debug_token', params=checked_params)
        return DebugTokenInfo(**response.json()['data'])
    debug_token_info = get_debug_token_info(access_token)

    user_info_fields = ['id', 'name', 'picture', 'email']
    url_graph_user_info = f'https://graph.facebook.com/me?'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token':access_token,
    }
    response = requests.get(url_graph_user_info, params=params_graph_user_info)
    result = response.json()
    user_info = UserInfo(data=result)

    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:

        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0,
        )
    django_login(request, user)
    return redirect('post:post_list')

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
