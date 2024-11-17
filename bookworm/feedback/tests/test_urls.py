from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from feedback.models import Feedback

User = get_user_model()


class FeedbackURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="feedback_user",
            email="feedback_user@gmail.com",
            password="feedback_user"
        )
        cls.feedback = Feedback.objects.create(
            author=cls.user,
            theme="suggestion",
            text="Test Text" * 10,
        )
        cls.template = {
            "feedback_create": "feedback/feedback_form.html",
            "feedback_created": "feedback/feedback_created.html"
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_exists_at_desired_location(self):
        """
        Check that urls are in the right
        place and return right statuses.
        """
        response_list = {
            reverse("feedback:feedback_create"):
            HTTPStatus.OK,

            reverse("feedback:feedback_created",
                    kwargs={"uuid": self.feedback.uuid}
                    ):
            HTTPStatus.OK,
        }
        for url, expected_status_code in response_list.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, expected_status_code)

    def test_urls_dont_allow_for_guest_user(self):
        """
        Check that urls are in the right
        place and return right statuses.
        """
        response_list = {
            reverse("feedback:feedback_create"):
            HTTPStatus.FOUND,

            reverse("feedback:feedback_created",
                    kwargs={"uuid": self.feedback.uuid}
                    ):
            HTTPStatus.FOUND,
        }
        for url, expected_status_code in response_list.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                print(url, response.status_code)
                self.assertEqual(response.status_code, expected_status_code)

    def test_urls_uses_correct_template(self):
        """URLs return correct html template."""
        template_url_names = {
            reverse("feedback:feedback_create"):
            self.template["feedback_create"],

            reverse("feedback:feedback_created",
                    kwargs={"uuid": self.feedback.uuid}
                    ):
            self.template["feedback_created"]
        }
        for url, expected_template in template_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, expected_template)
