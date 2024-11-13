from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client


User = get_user_model()


class UserURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="UserName",
            email="username@gmail.com",
            password="passwordusername"
        )
        cls.template = {
            "profile":
            "users/profile.html",

            "profile_comments":
            "users/comments.html",

            "login":
            "users/auth/login.html",

            "signup":
            "users/auth/signup.html",

            "password_change":
            "users/auth/password_change.html",

            "password_reset_complete":
            "users/auth/password_reset_complete.html",

            "password_reset_confirm":
            "users/auth/password_reset_confirm.html",

            "password_reset_done":
            "users/auth/password_reset_done.html",

            "password_reset":
            "users/auth/password_reset_form.html"
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_exists_at_desired_location(self):
        template_url_names = {
            reverse("users:profile"):
            HTTPStatus.OK,

            reverse("users:profile_comments"):
            HTTPStatus.OK,

            reverse("users:login"):
            HTTPStatus.OK,

            reverse("users:signup"):
            HTTPStatus.OK,

            reverse("users:password_change"):
            HTTPStatus.OK,

            reverse("users:password_reset"):
            HTTPStatus.OK,

            reverse("users:password_reset_done"):
            HTTPStatus.OK,

            reverse("users:password_reset_complete"):
            HTTPStatus.OK
        }
        for url, expected_status in template_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_urls_uses_correct_template(self):
        template_url_names = {
            reverse("users:profile"):
            self.template["profile"],

            reverse("users:profile_comments"):
            self.template["profile_comments"],

            reverse("users:login"):
            self.template["login"],

            reverse("users:signup"):
            self.template["signup"],

            reverse("users:password_change"):
            self.template["password_change"],

            reverse("users:password_reset"):
            self.template["password_reset"],

            reverse("users:password_reset_done"):
            self.template["password_reset_done"],

            reverse("users:password_reset_complete"):
            self.template["password_reset_complete"]
        }
        for url, expected_template in template_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, expected_template)