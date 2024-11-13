from typing import Optional

from django.contrib.auth import get_user_model

from logger.log import logger
from books.repository import book_repository, comment_repository
from books.models import Book, Comment


User = get_user_model()


class BookService:
    def __init__(self):
        self.repository = book_repository

    def create_book(
        self,
        title: str,
        image: str,
        publication_year: int,
        description: str = None,
        author: str = None,
    ) -> Optional[Book]:
        logger.info(f"Start creating book with args:"
                    f"{title=}, "
                    f"{image=}, "
                    f"{description=}, "
                    f"{author=}"
                    )
        try:
            book = self.repository.create_book(
                title=title,
                image=image,
                author=author,
                description=description,
                publication_year=publication_year
            )
            logger.info(f"Book created, {id=}")
            return book
        except Exception as er:
            logger.error(f"Book creation error: {er}")
            return None

    def get_all_books(self, **filter_by):
        logger.info(f"Get books {filter_by=}")
        books = self.repository.get_books(**filter_by)
        return books

    def search_books(self, q: str):
        logger.info(f"Search books {q=}")
        books = self.repository.search_books(q)
        return books

    def get_book_by_id(self, book_id: int) -> Book:
        logger.debug(f"Get book with {book_id=}")
        book = self.repository.get_book_by_id(book_id=book_id)
        if book:
            logger.debug(f"Update book {book.id!r} views")
            self.repository.update_book_views(book)
        return book

    def book_ty_title_exists(self, book_title: str) -> Optional[Book]:
        logger.debug(f"Get book with {book_title=}")
        book = self.repository.get_book_by_title(book_title)
        return book


class CommentService:
    def __init__(self):
        self.repository = comment_repository

    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        comment = self.repository.get_comment_by_id(comment_id)
        return comment

    def comments_by_user(self, user: User):
        logger.info(f"Get comments by {user=}")
        comments = self.repository.get_comments(author=user)
        return comments

    def search_comments(self, q: str, author: User = None):
        logger.info(f"Search comments {q=}, {author=}")
        comments = self.repository.search_comments(q=q, author=author)
        return comments

    def get_latest_comments(self, latest_count: int = 10, author: User = None):
        logger.info(f"Get latest {latest_count} comments, {author=}")
        comments = self.repository.get_latest_comments(
            latest_count=latest_count,
            author=author
        )
        return comments

    def delete_comment(self, user, comment):
        logger.info(f"Start delete comment {comment}")
        self.repository.delete_comment(comment.id)


book_service = BookService()
comment_service = CommentService()
