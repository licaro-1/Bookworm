from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Add test user in to db."""
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="Alex",
            email="alex@gmail.com",
            password="alexpassword"
        )

    def test_verbose_name(self):
        """Verbose name equal to expected."""
        field_verboses = {
            "username": "Юзернейм",
            "email": "Почта",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "is_active": "Активный аккаунт",
            "date_joined": "Дата регистрации",
            "last_login": "Последний вход",
            "avatar": "Аватар",
            "role": "Роль"
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.user._meta.get_field(field).verbose_name, expected_value
                )

    def test_model_have_correct_object_name(self):
        """Test model __str__ method."""
        self.assertEqual(
            self.user.__str__(),
            f"User({self.user.id}, {self.user.email})"
        )
