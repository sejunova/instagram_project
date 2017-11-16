from django.conf.urls import url

from ..apis import Login, SignUp, FacebookLogin

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='api-login'),
    url(r'^signup/$', SignUp.as_view(), name='api-signup'),
    url(r'^facebook-login/$', FacebookLogin.as_view(), name='api-facebook-login'),
]