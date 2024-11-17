from django.urls import path

from books import views

app_name = "books"


urlpatterns = [
    path("", views.index, name="index"),
    path("books/<int:id>/", views.personal_book, name="book_detail"),
    path(
        "books/comments/<int:comment_id>/",
        views.delete_comment,
        name="book_comment_delete"
    ),
]
