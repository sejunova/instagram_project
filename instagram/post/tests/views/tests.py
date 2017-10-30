from unittest import TestCase

from django.urls import reverse, resolve

from ... import views


class PostLikeToggleViewTest(TestCase):
    TEST_POST_PK = 1
    VIEW_URL = f'/post/{TEST_POST_PK}/like-toggle/'
    VIEW_URL_NAME = 'post:post-like-toggle'

    def test_url_equal_reverse_url_name(self):
        self.assertEqual(
            self.VIEW_URL,
            reverse(
                self.VIEW_URL_NAME, kwargs={
                    'post_pk': self.TEST_POST_PK}))

    def test_url_resolves_to_post_like_toggle_view(self):
        found = resolve(self.VIEW_URL)
        self.assertEqual(found.func, views.post_like_toggle)