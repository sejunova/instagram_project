from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=26, *args, **kwargs)
class User(AbstractUser):
    img_profile = models.ImageField('이미지 업로드', upload_to='user', blank=True)
    age = models.PositiveIntegerField('나이', null=True)
    like_posts = models.ManyToManyField('post.Post')

    objects = UserManager()

    class Meta:
        verbose_name = "사용자 이름"
        verbose_name_plural = f'{verbose_name} 목록'