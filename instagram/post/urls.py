from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/upload_pic/$', views.upload_pic, name='upload_pic'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
]