from typing import Optional
from django.db.models import Q
from django.contrib.auth import get_user_model

from books.models import Book, Comment


User = get_user_model()


class BookRepository:
    """Book repository."""

    def get_book_by_id(self, book_id:int):
        """Get book by id."""
        return Book.objects.filter(id=book_id).first()

    def get_book_by_title(self, title: str) -> Optional[Book]:
        """Get book by title."""
        return Book.objects.filter(title=title).first()

    def get_book_by_author(self, author: User) -> Optional[Book]:
        """Get book by author."""
        return Book.objects.filter(author=author).first()

    def get_books(self, **filter_by):
        """Get books by any filter/all books."""
        books = Book.objects.filter(**filter_by)
        return books

    def search_books(self, q: str):
        """Search books by title, description or author."""
        books = Book.objects.filter(
            Q(title__icontains=q)
            |
            Q(description__icontains=q)
            |
            Q(author__icontains=q)
        )
        return books

    def create_book(
        self,
        title: str,
        image: str,
        publication_year: int,
        author: str = None,
        description: str = None,
    ) -> Book:
        """Create book."""
        return Book.objects.create(
            title=title,
            image=image,
            author=author,
            description=description,
            publication_year=publication_year,
        )

    def update_book(self, book, **kwargs) -> Book:
        """Partial book update."""
        for key, val in kwargs.items():
            setattr(book, key, val)
        book.save()
        return book

    def update_book_views(self, book) -> Book:
        """Update book views."""
        book.views = book.views + 1
        book.save()
        return book

    def delete_book(self, book_id: int) -> None:
        """Delete book"""
        return Book.objects.filter(id=book_id).delete()


class CommentRepositoy:
    """Comment repository."""
    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by id."""
        comment = Comment.objects.filter(id=comment_id).first()
        return comment

    def get_comments(self, **filter_by):
        """Get comments by filters/all comments."""
        comments = Comment.objects.filter(**filter_by)
        return comments

    def get_latest_comments(self, latest_count: int, author: User = None):
        """Get latest comments of all/by user."""
        if author:
            comments = Comment.objects.filter(author=author)[:latest_count]
        else:
            comments = Comment.objects.all()[:latest_count]
        return comments

    def search_comments(self, q: str, author: User = None):
        """Search comments by text or book_title"""
        comments = Comment.objects.filter(
            Q(text__icontains=q)
            |
            Q(book__title__icontains=q)
        )
        if author:
            comments = comments.filter(author=author)
        return comments

    def delete_comment(self, comment_id: int) -> None:
        """Delete comment by id."""
        Comment.objects.filter(id=comment_id).delete()


book_repository = BookRepository()
comment_repository = CommentRepositoy()