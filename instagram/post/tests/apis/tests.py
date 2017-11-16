import filecmp
import io
import os
from random import randint

from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from config import settings
from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/apis/post/'
    VIEW = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username)

    @staticmethod
    def create_post(author=None):
        return Post.objects.create(author=author, photo=File(io.BytesIO()))

    def test_post_list_url(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve(self):
        resolver_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(resolver_match.url_name, self.URL_API_POST_LIST_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW)

    def test_get_post_list(self):
        user = self.create_user()
        num = randint(3, 20)
        for i in range(num):
            self.create_post(author=user)
        url = reverse(self.URL_API_POST_LIST_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), num)
        self.assertEqual(len(response.data), num)

        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('id', cur_post_data)  # 왜 나는 'id'? 왜냐하면 serializer에 id라고 했으니까!
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_at', cur_post_data)

    def test_get_post_list_exclude_author_is_none(self):
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)

        response = self.client.get(self.URL_API_POST_LIST)
        self.assertEqual(len(response.data), num_posts)

    # def test_create_post(self):
    #     user = self.create_user(username='dummy')
    #     factory = APIRequestFactory()
    #     f = self.generate_photo_file()
    #     request = factory.post(self.URL_API_POST_LIST,
    #                            {'photo':f, 'created_at':datetime.now()})
    #     force_authenticate(request, user=user)
    #
    #     view = PostList.as_view()
    #     response = view(request)
    #     self.assertTrue(response.data, Post.objects.last())

    def test_create_post(self):
        user = self.create_user(username='dummy')
        self.client.force_authenticate(user=user)
        path = os.path.join(settings.STATIC_DIR, 'test', 'isihara.jpg')
        with open(path, 'rb') as photo:
            response = self.client.post(self.URL_API_POST_LIST, {
                'photo':photo,
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.get(pk=response.data['id'])
        print(post.photo.file.name)
        self.assertTrue(filecmp.cmp(path, post.photo.file.name))
        post.photo.delete()