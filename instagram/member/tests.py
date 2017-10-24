from django.contrib.auth import authenticate
from django.test import TestCase, TransactionTestCase

from .models import User

class UserModelTest(TransactionTestCase):
    DUMMY_USERNAME = 'username'
    DUMMY_PASSWORD = 'password'
    DUMMY_AGE = 25

    def test_fields_default_value(self):
        user = User.objects.create_user(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
            age=self.DUMMY_AGE
        )
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.username, self.DUMMY_USERNAME)
        self.assertEqual(user.img_profile, '')
        self.assertEqual(user.age, self.DUMMY_AGE)
        self.assertEqual(user.following_users.count(), 0)

        self.assertEqual(user, authenticate(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
        ))

    def test_follow(self):
        mina, hyeri, yura, sojin = [User.objects.create_user(
            username=f'{name}',
            age=0
        ) for name in ['민아', '혜리', '유라', '소진']]


        mina.follow_toggle(hyeri)
        mina.follow_toggle(yura)
        mina.follow_toggle(sojin)

        hyeri.follow_toggle(yura)
        hyeri.follow_toggle(sojin)

        yura.follow_toggle(sojin)


        self.assertEqual(mina.following_users.count(), 3)
        self.assertEqual(hyeri.following_users.count(), 2)
        self.assertEqual(yura.following_users.count(), 1)
        self.assertEqual(sojin.following_users.count(), 0)


        self.assertIn(hyeri, mina.following_users.all())
        self.assertIn(yura, mina.following_users.all())
        self.assertIn(sojin, mina.following_users.all())

        self.assertIn(yura, hyeri.following_users.all())
        self.assertIn(sojin, hyeri.following_users.all())

        self.assertIn(sojin, yura.following_users.all())