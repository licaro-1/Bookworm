import os
import json

from django.core.management.base import BaseCommand, CommandError

from logger.log import logger
from bookworm.settings import BASE_DIR
from books.repository import BookRepository


LOAD_PATH = os.path.join(BASE_DIR, "books", "management", "upload_files")


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
        logger.info(f"Start execution command load_books with args: {filename=}")
        full_file_path = os.path.join(LOAD_PATH, filename)
        if not os.path.isfile(full_file_path):
            logger.info(f"File with name {filename!r} does not exists.")
            raise CommandError(f"File {filename} does not exists")
        if not filename.endswith(".json"):
            raise CommandError(f"Only `.json` files are supported")
        count_created = 0
        strip_if_exists = lambda x: x.strip() if x else None
        with open(full_file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
            for book in data:
                book_title = strip_if_exists(book.get("title"))
                book_author = strip_if_exists(book.get("author"))
                book_description = strip_if_exists(book.get("description"))
                book_public_date = book.get("public_date")
                book_image = book.get("image_url")
                if not book_title or not book_image or self.book_repository.get_book_by_title(book_title):
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
        self.stdout.write(f"Command execution is complete, books have been added: {count_created}")
        return 0
