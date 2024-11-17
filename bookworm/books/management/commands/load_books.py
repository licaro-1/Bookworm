import json
import os
from typing import Optional

from django.core.management.base import BaseCommand, CommandError

from books.repository import BookRepository
from bookworm.settings import BASE_DIR
from logger.log import logger

LOAD_PATH = os.path.join(BASE_DIR, "books", "management", "upload_files")


def strip_string_if_exists(string: str = None) -> Optional[str]:
    if string:
        return string.strip()
    return None


class Command(BaseCommand):
    """Class for cli - load books in to db."""
    help = "Load books in to db from the transferred file (only json format)."
    book_repository = BookRepository()

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str, help="Filename for upload")

    def handle(self, *args, **options):
        filename = options["filename"]
        if not filename:
            raise CommandError("Filename is required")
        logger.info(
            f"Start execution command load_books with args: {filename=}"
        )
        full_file_path = os.path.join(LOAD_PATH, filename)
        if not os.path.isfile(full_file_path):
            logger.info(f"File with name {filename!r} does not exists.")
            raise CommandError(f"File {filename} does not exists")
        if not filename.endswith(".json"):
            raise CommandError("Only `.json` files are supported")
        count_created = 0
        with open(full_file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
            for book in data:
                book_title = strip_string_if_exists(book.get("title"))
                book_author = strip_string_if_exists(book.get("author"))
                book_description = strip_string_if_exists(
                    book.get("description")
                )
                if book_description and len(book_description) > 4000:
                    self.stdout.write(
                        f"Book with title {book_title} have len "
                        f"description great then 4000, and will "
                        f"not save to database"
                    )
                    continue
                book_public_date = book.get("public_date")
                book_image = book.get("image_url")
                if not book_title or not book_image or \
                        self.book_repository.get_book_by_title(book_title):
                    continue
                book = self.book_repository.create_book(
                    title=book_title,
                    image=book_image,
                    publication_year=book_public_date,
                    author=book_author,
                    description=book_description,
                )
                count_created += 1
                self.stdout.write(f"Add book to db with: {book}")
        self.stdout.write(
            f"Command execution is complete, "
            f"books have been added: {count_created}"
        )
        return 0
