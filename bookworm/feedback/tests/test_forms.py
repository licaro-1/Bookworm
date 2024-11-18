from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from feedback.models import Feedback

User = get_user_model()


class FeedbackCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testuserpassword"
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @patch('django_recaptcha.fields.ReCaptchaField.clean', return_value=None)
    def test_feedback_create(self, mock_clean):
        mock_clean.return_value = 'mocked_success'
        form_data = {
            "theme": "suggestion",
            "text": "Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit, sed do eiusmod tempor "
                    "incididunt ut labore et dolore magna aliqua. "
                    "Ut enim ad minim veniam, quis nostrud "
                    "exercitation ullamco laboris nisi ut aliquip "
                    "ex ea commodo consequat. Duis aute irure dolor "
                    "in reprehenderit in voluptate velit esse cillum "
                    "dolore eu fugiat nulla pariatur"
        }
        response = self.authorized_client.post(
            reverse("feedback:feedback_create"),
            data=form_data,
            follow=True
        )
        self.assertTrue(Feedback.objects.filter(
            author=self.user,
            theme=form_data["theme"],
            text=form_data["text"]
        ).exists()
        )
        feedback = Feedback.objects.filter(
            author=self.user,
            theme=form_data["theme"],
            text=form_data["text"]
        ).first()
        self.assertRedirects(
            response,
            reverse(
                "feedback:feedback_created",
                kwargs={"uuid": feedback.uuid}
            )
        )
