from django.db import models

from config import settings

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(author=None)
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               related_name='posts',
                               blank=True,
                               null=True)
    #유저모델 이름 신경쓸 필요 X 어차피 유저모델은 하나다
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return f'{self.created_at}'

    class Meta:
        ordering = ['-created_at']

class PostComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                                )
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at}'

    class Meta:
        ordering = ['created_at']