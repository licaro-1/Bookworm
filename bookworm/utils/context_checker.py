from books.models import Book, Comment


def book_context_checker(
        self,
        object: Book,
        expected_obj: Book
):
    """Check context of Book object."""
    context_obj = {
        expected_obj.title: object.title,
        expected_obj.description: object.description,
        expected_obj.publication_year: object.publication_year,
        expected_obj.image: object.image
    }
    return _context_checker(self, context_obj)


def comment_context_checker(
        self,
        object: Comment,
        expected_obj: Comment
):
    """Check context of Comment object."""
    context_obj = {
        expected_obj.author: object.author,
        expected_obj.text: object.text,
        expected_obj.rating: object.rating,
        expected_obj.recommended: object.recommended,
        expected_obj.book: object.book
    }
    return _context_checker(self, context_obj)


def _context_checker(self, context_obj: dict):
    """Check context of transferred object."""
    for expected_value, response_value in context_obj.items():
        with self.subTest(expected_value=expected_value):
            self.assertEqual(expected_value, response_value)
