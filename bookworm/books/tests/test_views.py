from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from books.forms import CommentCreateForm
from books.models import Book, Comment
from bookworm.settings import (PAGINATION_OBJ_PER_PAGE, S3_DIR_BOOK_COVERS_URL,
                               S3_DIR_USER_IMAGES_URL)
from utils.context_checker import book_context_checker, comment_context_checker

User = get_user_model()


class BookPagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="NanoName",
            email="nanoname@gmail.com",
            password="nanonamepas"
        )
        # create book for search test
        cls.book = Book.objects.create(
            creator=cls.user,
            title="Book Title Test",
            publication_year=2021,
            description="Book Description",
            image="testing1.jpg"
        )
        cls.comment = Comment.objects.create(
            book=cls.book,
            author=cls.user,
            text="Test Comment",
            rating=2,
            recommended=True
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_context(self):
        response = self.guest_client.get(reverse("books:index"))
        book_context_checker(
            self,
            response.context.get("page_obj")[0],
            self.book
        )
        self.assertEqual(
            response.context.get("S3_DIR_BOOK_COVERS_URL"),
            S3_DIR_BOOK_COVERS_URL
        )

    def test_book_detail_context(self):
        response = self.guest_client.get(
            reverse("books:book_detail", kwargs={"id": self.book.id})
        )
        book_context_checker(
            self,
            response.context.get("book"),
            self.book
        )
        comment_context_checker(
            self,
            response.context.get("book_comments_page_obj")[0],
            self.comment
        )
        self.assertEqual(
            response.context.get("S3_DIR_BOOK_COVERS_URL"),
            S3_DIR_BOOK_COVERS_URL
        )
        self.assertEqual(
            response.context.get("S3_DIR_USER_IMAGES_URL"),
            S3_DIR_USER_IMAGES_URL
        )
        self.assertIsInstance(
            response.context.get("comment_create_form"),
            CommentCreateForm
        )

    def test_index_search(self):
        linux_book = Book.objects.create(
            author=self.user,
            title="Linux Book",
            publication_year=2021,
            description="Linux Book Description",
            image="testing1.jpg"
        )
        response = self.guest_client.get(
            reverse("books:index") + "?q=Linux"
        )
        # test that only 1 book was found on the search
        self.assertEqual(
            len(response.context.get("page_obj")),
            1
        )
        # test that the book found matches the search query
        book_context_checker(
            self,
            response.context.get("page_obj")[0],
            linux_book
        )


class PaginatorViewsTest(TestCase):
    """
    Test pagination work correct on index
    and book detail pages.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="NoNameAuthor",
            email="nonameauthor@gmail.com",
            password="nonameauthor"
        )
        cls.BOOK_CREATING_COUNT = 12
        cls.BOOK_COMMENT_CREATING_COUNT = 12

    def setUp(self):
        self.guest_client = Client()
        #  Creating books for test paginator on index page
        books = []
        for book_number in range(1, self.BOOK_CREATING_COUNT + 1):
            books.append(
                Book(
                    title=f"Test Book #{book_number}",
                    publication_year=2000,
                    description="Test Book Description",
                    image=f"testing{book_number}.jpg"
                )
            )
        Book.objects.bulk_create(books)
        # Creating comment for test paginator on book detail page
        comments = []
        book = Book.objects.get(pk=1)
        for comment_number in range(1, self.BOOK_COMMENT_CREATING_COUNT + 1):
            comments.append(
                Comment(
                    book=book,
                    author=self.user,
                    text=f"Comment #{comment_number}",
                    rating=4,
                    recommended=True
                )
            )
        Comment.objects.bulk_create(comments)

    def test_first_index_page_contains_ten_records(self):
        response = self.guest_client.get(reverse("books:index"))
        self.assertEqual(
            len(response.context["page_obj"]),
            PAGINATION_OBJ_PER_PAGE
        )

    def test_second_index_page_contains_two_records(self):
        response = self.guest_client.get(
            reverse("books:index") + "?page=2"
        )
        self.assertEqual(
            len(response.context["page_obj"]),
            2
        )

    def test_first_book_comment_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse("books:book_detail", kwargs={"id": 1})
        )
        self.assertEqual(
            len(response.context.get("book_comments_page_obj")),
            PAGINATION_OBJ_PER_PAGE
        )

    def test_second_book_comment_page_contains_two_records(self):
        response = self.guest_client.get(
            reverse("books:book_detail", kwargs={"id": 1}) + "?page=2"
        )
        self.assertEqual(
            len(response.context.get("book_comments_page_obj")),
            2
        )
