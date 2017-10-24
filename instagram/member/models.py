from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=26, *args, **kwargs)
class User(AbstractUser):
    img_profile = models.ImageField('이미지 업로드', upload_to='user', blank=True)
    age = models.PositiveIntegerField('나이', null=True)
    like_posts = models.ManyToManyField('post.Post')
    # user 객체에서 이걸 사용하면 user 객체가 반환
    following_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='followers',
    )

    objects = UserManager()

    class Meta:
        verbose_name = "사용자 이름"
        verbose_name_plural = f'{verbose_name} 목록'

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        if relation_created:
            return True
        relation.delete()
        return False

class Relation(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        #user 객체에서 이것을 사용하면 relation 객체가 반환
        related_name='following_user_relations'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # user 객체에서 이것을 사용하면 relation 객체가 반환
        related_name='follower_relations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation ('\
                f'from : {self.from_user.username}, '\
                f'to: {self.to_user.username})'