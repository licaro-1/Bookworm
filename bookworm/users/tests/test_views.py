from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from books.models import Book, Comment
from utils.context_checker import comment_context_checker
from bookworm.settings import (
    S3_DIR_USER_IMAGES_URL,
    S3_DIR_BOOK_COVERS_URL
)


User = get_user_model()


class UserPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="Bob",
            email="bob@gmail.com",
            password="bobpassword"
        )
        cls.book = Book.objects.create(
            creator=cls.user,
            title="Bob Book Title",
            publication_year=2023,
            description="Book Description",
            image="testing.jpg"
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            book=cls.book,
            text="Bob Unique comment text",
            rating=4,
            recommended=True,
        )
        cls.comment_context_checker = comment_context_checker

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_profile_context(self):
        response = self.authorized_client.get(
            reverse("users:profile")
        )
        self.comment_context_checker(
            response.context.get("latest_comments")[0],
            self.comment
        )
        self.assertEqual(
            response.context.get("user"),
            self.user
        )
        self.assertEqual(
            response.context.get("S3_DIR_USER_IMAGES_URL"),
            S3_DIR_USER_IMAGES_URL
        )
        self.assertEqual(
            response.context.get("S3_DIR_BOOK_COVERS_URL"),
            S3_DIR_BOOK_COVERS_URL
        )

    def test_user_comments_context(self):
        response = self.authorized_client.get(
            reverse("users:profile_comments")
        )
        self.assertEqual(
            response.context.get("user"),
            self.user
        )
        self.comment_context_checker(
            response.context.get("page_obj")[0],
            self.comment
        )
        self.assertEqual(
            response.context.get("S3_DIR_BOOK_COVERS_URL"),
            S3_DIR_BOOK_COVERS_URL
        )

    def test_user_comments_search(self):
        # Create comments to check if the search is correct
        for comment_number in range(1, 5):
            Comment.objects.create(
                author=self.user,
                book=self.book,
                text=f"Comment #{comment_number}",
                rating=3,
                recommended=False
            )
        # Looking for a comment with a unique value
        response = self.authorized_client.get(
            reverse("users:profile_comments") + "?q=Bob Unique"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.context.get("page_obj")),
            1
        )
        self.assertEqual(
            response.context.get("page_obj")[0],
            self.comment
        )


class PaginationViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="alexname",
            email="alexname@gmail.com",
            password="alexpassword"
        )
        cls.book = Book.objects.create(
            creator=cls.user,
            author="Josh Alos",
            title="Book Title",
            description="Perfect Book Description",
            publication_year=2000
        )
        cls.COMMENT_CREATING_COUNT = 12

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for comment_number in range(1, self.COMMENT_CREATING_COUNT + 1):
            Comment.objects.create(
                author=self.user,
                book=self.book,
                text=f"Its comment #{comment_number}",
                rating=4,
                recommended=False
            )

    def test_first_user_comments_page_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse("users:profile_comments")
        )
        self.assertEqual(
            len(response.context.get("page_obj")),
            10
        )

    def test_second_user_comments_page_contains_two_records(self):
        response = self.authorized_client.get(
            reverse("users:profile_comments") + "?page=2"
        )
        self.assertEqual(
            len(response.context.get("page_obj")),
            2
        )