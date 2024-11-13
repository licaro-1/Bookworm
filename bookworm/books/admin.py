from django.contrib import admin

from bookworm.admin import bookworm_admin_site
from books.models import Book, Comment


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "views",
        "author",
        "description",
        "image",
    )
    search_fields = ("title", "author",)
    empty_value_display = "Пусто"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "created_at",
        "book",
        "text",
        "rating",
        "recommended",
    )
    search_fields = ("author", "book", "text")
    empty_value_display = "Пусто"


bookworm_admin_site.register(Book, BookAdmin)
bookworm_admin_site.register(Comment, CommentAdmin)
