from django.test import TestCase

from books.models import Book


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Add test book in to db."""
        cls.book = Book.objects.create(
            title="Book Title",
            publication_year=2020,
            description="Book Description",
            image="testing.jpg",
        )

    def test_verbose_name(self):
        """Verbose name equal to expected."""
        field_verboses = {
            "title": "Название",
            "description": "Описание",
            "publication_year": "Год публикации",
            "image": "Изображение",
            "views": "Просмотры",
            "created_at": "Дата добавления"
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.book._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_model_have_correct_object_name(self):
        """Test model __str__ method."""
        self.assertEqual(
            self.book.__str__(),
            f"Book({self.book.title}, {self.book.publication_year})"
        )
