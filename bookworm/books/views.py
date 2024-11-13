from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseForbidden
from django.views.decorators.http import require_http_methods

from django.urls import reverse_lazy

from bookworm.settings import (
    S3_DIR_BOOK_COVERS_URL,
    S3_DIR_USER_IMAGES_URL
)
from utils.pagination import paginator
from logger.log import logger
from books.forms import CommentCreateForm
from books.service import book_service, comment_service


def index(request):
    """
    Index page view
    Processing creating book by moderator or admin
    and output all books from new to old.
    """
    q = request.GET.get("q")
    if q:
        books = book_service.search_books(q)
    else:
        books = book_service.get_all_books()
    page_obj = paginator(request, books)
    context = {
        "page_obj": page_obj,
        "S3_DIR_BOOK_COVERS_URL": S3_DIR_BOOK_COVERS_URL,
    }
    return render(request, "books/index.html", context)


def personal_book(request, id: int):
    """
    Personal book page view
    Processing the form for editing or creating comment
    Output book info and all comments with pagination.
    """
    book = book_service.get_book_by_id(book_id=id)
    if not book:
        raise Http404()
    comment_create_form = CommentCreateForm()
    # if comment_id -> set instance to comment form
    comment_id = request.GET.get("comment_id") or request.POST.get("comment_id")
    comment_to_edit = None
    if comment_id:
        comment_to_edit = comment_service.get_comment_by_id (comment_id)
        if not comment_to_edit:
            raise Http404()
    if (
            comment_to_edit
            and
            request.user.is_authenticated
            and
            comment_to_edit.author == request.user
    ):
        comment_create_form = CommentCreateForm(instance=comment_to_edit)
    if request.method == "POST":
        logger.info(f"Received POST data: {request.POST}")
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("users:login"))
        if comment_to_edit and comment_to_edit.author != request.user:
            return HttpResponseForbidden()
        if comment_to_edit:
            comment_create_form = CommentCreateForm(
                request.POST,
                instance=comment_to_edit
            )
            logger.info(f"Start updating comment "
                        f"with data {comment_to_edit.id}"
            )
        else:
            comment_create_form = CommentCreateForm(request.POST)
            logger.info(f"Start creating comment "
                        f"by {request.user}"
            )
        if comment_create_form.is_valid():
            comment = comment_create_form.save(commit=False)
            comment.book = book
            if comment_id:
                comment.is_edited = True
                comment.author = comment_to_edit.author
            else:
                comment.author = request.user
            comment.save()
            if comment_to_edit:
                logger.info(f"Success comment update, data={comment!r}")
            else:
                logger.info(f"Success comment create, data={comment!r}")
            return redirect(reverse_lazy("books:book_detail", kwargs={'id': id}))
    book_comments = paginator(request, book.comments.all())
    context = {
        "book": book,
        "S3_DIR_BOOK_COVERS_URL": S3_DIR_BOOK_COVERS_URL,
        "comment_create_form": comment_create_form,
        "book_comments_page_obj": book_comments,
        "S3_DIR_USER_IMAGES_URL": S3_DIR_USER_IMAGES_URL,
        "comment_id": comment_id,
    }
    return render(request, "books/book_detail.html", context)


@require_http_methods(["POST"])
def delete_comment(request, comment_id: int):
    """
    Delete comment by post method and redirect
    to previous url/all_comments_by_user.
    """
    comment = comment_service.get_comment_by_id(comment_id)
    if not comment:
        raise Http404()
    if (comment.author != request.user
            and not (request.user.is_moderator or request.user.is_admin)):
        return HttpResponseForbidden()
    comment_service.delete_comment(request.user, comment)
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)
    return redirect("users:profile_comments")
