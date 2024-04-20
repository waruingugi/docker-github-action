from django.test import TestCase
import secrets
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="dummy@gmail.com",
            password=secrets.token_urlsafe(10)
        )
        # This test passes
        self.assertTrue(user.is_active)

    def test_this_fails(self):
        user = User.objects.create_user(
            email="dummy@gmail.com",
            password=secrets.token_urlsafe(10)
        )
        # This test fails
        self.assertTrue(user.is_staff)
