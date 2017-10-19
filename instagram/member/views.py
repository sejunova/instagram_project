from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from member.forms import SignUpForm, LoginForm

User = get_user_model() #User가 어디서 온건지 명확히 알 수 있다..?
def signup_old(request): #forms.py 안쓰고 할 때
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
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.signup()
            # username = member_form.cleaned_data['username']
            # password = password=member_form.cleaned_data['password']
            # # 아래 과정은 이제 없어도 된다. 왜? forms.py에 클래스안에 검증메소드 추가함.
            # # if User.objects.filter(username=username).exists():
            # #     return HttpResponse(f' Username {username} already exists.')
            # user = User.objects.create_user(
            #     username=username,
            #     password=password,
            # )
            return HttpResponse(f'{user.username} {user.password}')
    signup_form = SignUpForm()
    context = {
        'member_form': signup_form,
    }
    return render(request, 'member/signup.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.login(request)
            return redirect('post_list')
        else:
            return HttpResponse('Login credentials invalid')
    else:
        login_form = LoginForm()
    context = {
        'login_form':login_form,
    }
    return render(request, 'member/login.html', context)

def logout(request):
    django_logout(request)
    return redirect('post_list')