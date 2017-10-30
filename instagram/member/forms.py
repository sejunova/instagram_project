from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()  ## 여기다 유저 호출해주는게 convention인듯

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'img_profile', 'age', 'nickname')
        widgets = {
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    # def clean_username(self):
    #     super().clean_username()
    #     username = self.cleaned_data['username']
    #     if username.startswith('fb_'):
    #         raise forms.ValidationError("Username can't start with fb_")

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





