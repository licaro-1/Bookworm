from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from bookworm.settings import S3_DIR_BOOK_COVERS
from books.models import Comment, Book
from utils.context_checker import comment_context_checker
from s3.client import bookworm_s3_client


User = get_user_model()


class CommentCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="NoNameUser",
            email="nonameuser@gmail.com",
            password="nonameuser2"
        )
        cls.book = Book.objects.create(
            creator=cls.user,
            title="Book Title Test",
            publication_year=2021,
            description="Book Description",
            image="testing1.jpg"
        )
        cls.comment_for_update = Comment.objects.create(
            book=cls.book,
            author=cls.user,
            text=f"Test Comment",
            rating=2,
            recommended=True
        )
        cls.comment_context_checker = comment_context_checker

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_comment_create(self):
        comment_cont = Comment.objects.count()
        form_data = {
            "text": "Lorem ipsum dolor sit amet, "
                    "consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt "
                    "ut labore et dolore magna aliqua. "
                    "Ut enim ad minim veniam, quis nostrud "
                    "exercitation ullamco",
            "recommended": True,
            "rating": 4
        }
        response = self.authorized_client.post(
            reverse("books:book_detail", kwargs={"id": self.book.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            Comment.objects.count(),
            comment_cont + 1
        )
        self.assertTrue(
            Comment.objects.filter(**form_data).exists()
        )

    def test_comment_update(self):
        comment_id = self.comment_for_update.id
        comments_count = Comment.objects.count()
        new_comment_data = {
            "rating": 2,
            "recommended": False,
            "text": (
                "Lorem Ipsum is simply dummy text of the printing"
                "and typesetting industry. "
                "Lorem Ipsum has been the industry's standard"
            )
        }
        # Create expected comment object
        # after updating
        expected_obj = Comment(
            author=self.user,
            book=self.book,
            **new_comment_data
        )
        response = self.authorized_client.post(
            reverse("books:book_detail", kwargs={"id": self.book.id}),
            data={
                "comment_id": comment_id,
                **new_comment_data
            },
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Check that a new comment is not created
        self.assertEqual(comments_count, Comment.objects.count())
        self.comment_for_update.refresh_from_db()
        self.comment_context_checker(
            self.comment_for_update,
            expected_obj
        )


class BookCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="NoNameUser1",
            email="nonameuser1@gmail.com",
            password="nonameuserpassword"
        )
        cls.user.role = "moderator"
        cls.image_name = "book_cover.jpg"

    @classmethod
    def tearDownClass(cls):
        bookworm_s3_client.delete_file_from_s3(
            cls.image_name,
            S3_DIR_BOOK_COVERS
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_book_create(self):
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
            name=self.image_name,
            content=jpeg_bytes,
            content_type="image/jpeg"
        )
        form_data = {
            "title": "Book title",
            "description": "Book description",
            "publication_year": 2020,
            "image": uploaded
        }
        response = self.authorized_client.post(
            reverse("users:profile"),
            data={
                "add_book": True,
                **form_data
            },
            follow=True
        )
        self.assertTrue(Book.objects.filter(title=form_data.get("title")).exists())
        book = Book.objects.get(title=form_data.get("title"))
        self.assertRedirects(response, reverse("books:book_detail", kwargs={"id": book.id}))