from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()  ## 여기다 유저 호출해주는게 convention인듯


class SignUpForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):  # 기본적인 validity는 확보한 상태(ex) 문자열 와야하는데 숫자가 왔다거나..)
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("This account already exists")
        return data

    def clean_password2(self):  # clean_password로 하면 안되는 이유는 아직 password2에 대한 유효성 검사가 안된 시점이기때문
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Two passwords should be identical')
        return password2

    def clean(self):
        super().clean()
        if self.is_valid():
            setattr(self, 'signup', self._signup)

    def _signup(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        return User.objects.create_user(
            username=username,
            password=password,
        )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        # clean호출 즉, view에서 is_valied()없이 바로 login 메소드 호출하면 self.user가 없어서 오류나는것을 방지

    def clean(self):  # 2개 이상의 필드에 대한 유효성 검사
        cleaned_data = super().clean()  # 부모클래스의 유효성검사는 다 통과했다는 뜻
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        self.user = authenticate(username=username, password=password)
        if not self.user:
            raise forms.ValidationError('Unvalied authentication')
        else:
            setattr(self, 'login', self._login)  # 이때 아래 메소드를 login으로 호출 가능하게 해줌.

    def _login(self, request):
        django_login(request, self.user)
