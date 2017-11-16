from django.conf.urls import url, include

from utils.sms.apis import SendSMS

urlpatterns = [
    url(r'^post/', include('post.urls.apis', namespace='member')),
    url(r'^member/', include('member.urls.apis', namespace='post')),
    url(r'^utils/sms/send/$', SendSMS.as_view()),
]
