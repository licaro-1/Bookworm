from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from bookworm.settings import S3_DIR_USER_IMAGES
from s3.client import bookworm_s3_client
from users.forms import CreationForm

User = get_user_model()


class UserCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = CreationForm

    def setUp(self):
        self.guest_client = Client()

    @patch('django_recaptcha.fields.ReCaptchaField.clean', return_value=None)
    def test_user_register(self, mock_clean):
        mock_clean.return_value = 'mocked_success'
        form_data = {
            "username": "UserNameReg",
            "email": "usernamereg@gmail.com",
            "password": "usernamereg"
        }
        response = self.guest_client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(
            User.objects.filter(
                username=form_data["username"],
                email=form_data["email"]
            ).exists()
        )


class UserUpdateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="UserNoName",
            email="usernameee@gmail.com",
            password="usernameepassword"
        )
        cls.avatar_image_name = "avatar.jpg"

    @classmethod
    def tearDownClass(cls):
        bookworm_s3_client.delete_file_from_s3(
            cls.avatar_image_name,
            S3_DIR_USER_IMAGES
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_user_update(self):
        jpeg_bytes = (
            b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46'
            b'\x49\x46\x00\x01\x01\x01\x00\x60'
            b'\x00\x60\x00\x00\x00\xFF\xDB\x00'
            b'\x43\x00\x03\x02\x02\x03\x02\x02'
            b'\x03\x03\x03\x03\x04\x03\x03\x04'
            b'\x05\x08\x05\x05\x04\x04\x05\x09'
            b'\x09\x05\x0A\x14\x0F\x0C\x0A\x10'
            b'\x0C\x0A\x14\x10\x14\x18\x18\x18'
            b'\x20\x1A\x1A\x1A\x1E\x28\x1E\x34'
            b'\x34\x34\x38\x38\x38\x3C\x3C\x3C'
            b'\x40\x40\x40\x48\x48\x48\x50\x50'
            b'\x50\x58\x58\x58\x60\x60\x60\x68'
            b'\x68\x68\x70\x70\x70\x78\x78\x78'
            b'\x80\x80\x80\x88\x88\x88\x90\x90'
            b'\x90\x98\x98\x98\xA0\xA0\xA0\xA8'
            b'\xA8\xA8\xB0\xB0\xB0\xB8\xB8\xB8'
            b'\xC0\xC0\xC0\xC8\xC8\xC8\xD0\xD0'
            b'\xD0\xD8\xD8\xD8\xE0\xE0\xE0\xE8'
            b'\xE8\xE8\xF0\xF0\xF0\xF8\xF8\xF8'
            b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
        )
        uploaded = SimpleUploadedFile(
            name=self.avatar_image_name,
            content=jpeg_bytes,
            content_type="image/jpeg"
        )
        form_data = {
            "update_profile": True,
            "username": "UpdatedUsername",
            "first_name": "First_Name",
            "last_name": "Last_Name",
            "avatar": uploaded
        }
        users_count = User.objects.count()
        response = self.authorized_client.post(
            reverse("users:profile"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("users:profile"))
        # Check that the update does not create new user
        self.assertEqual(users_count, User.objects.count())
        # Check that the update was successful
        self.assertTrue(
            User.objects.filter(
                username=form_data["username"],
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
                avatar=form_data["avatar"]
            ).exists()
        )
