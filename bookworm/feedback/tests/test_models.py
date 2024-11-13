from django.test import TestCase

from feedback.models import Feedback
from users.models import User


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Add test feedback in to db."""
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="feedbackauthor",
            email="feedbackauthor@gmail.com",
            password="feedbackauthor"
        )
        cls.feedback = Feedback.objects.create(
            author=cls.user,
            theme="other",
            text="Test Feedback Text" * 4
        )

    def test_verbose_name(self):
        """Verbose name equal to expected."""
        field_verboses = {
            "theme": "Тема",
            "author": "Автор",
            "text": "Описание",
            "created_at": "Дата создания"
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.feedback._meta.get_field(field).verbose_name,
                    expected_value
                )