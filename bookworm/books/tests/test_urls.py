from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from books.models import Book


User = get_user_model()


class BookURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create book, user and template list
        """
        super().setUpClass()
        cls.book = Book.objects.create(
            title="Test Book Title",
            publication_year=2000,
            description="Test Description",
            image="test_img.jpg"
        )
        cls.user = User.objects.create_user(
            username="test_username",
            email="test@gmail.com",
            password="testpassword"
        )
        cls.template = {
            "index": "books/index.html",
            "book_detail": "books/book_detail.html"
        }

    def setUp(self):
        """
        Setup guest and authorized client.
        """
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_reverse_create_correct_url(self):
        """Check that reverse return expected url."""
        template_urls = {
            reverse("books:index"):
            "/",

            reverse("books:book_detail", kwargs={"id": self.book.id}):
            "/books/1/",
        }
        for reversed_url, expected_url in template_urls.items():
            with self.subTest(expected_url=expected_url):
                self.assertEqual(reversed_url, expected_url)

    def test_urls_exists_at_desired_location(self):
        """
        Check that urls are in the right
        place and return right statuses.
        """
        response_list = {
            reverse("books:index"):
            HTTPStatus.OK,

            reverse("books:book_detail", kwargs={"id": self.book.id}):
            HTTPStatus.OK,

            reverse("books:book_detail", kwargs={"id": 1000}):
            HTTPStatus.NOT_FOUND
        }
        for url, expected_status_code in response_list.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, expected_status_code)

    def test_urls_uses_correct_template(self):
        """URLs return correct html template."""
        template_url_names = {
            reverse("books:index"):
            self.template["index"],

            reverse("books:book_detail", kwargs={"id": self.book.id}):
            self.template["book_detail"]
        }
        for url, expected_template in template_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, expected_template)
