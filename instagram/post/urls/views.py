from django.conf.urls import url
from .. import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_pk>\d+)/comment_create', views.comment_create, name='comment_create'),
    url(r'^(?P<post_pk>\d+)/post_delete', views.post_delete, name='post_delete'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^(?P<post_pk>\d+)/like-toggle/', views.post_like_toggle, name='post_like_toggle'),
]
