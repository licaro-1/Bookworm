from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from bookworm.settings import (
    S3_DIR_USER_IMAGES_URL,
    S3_DIR_BOOK_COVERS_URL
)

from books.forms import BookCreateForm
from users.forms import CreationForm, CustomLoginForm, UserUpdateForm
from books.service import comment_service
from utils.pagination import paginator
from logger.log import logger


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/auth/signup.html"


class Login(LoginView):
    form_class = CustomLoginForm
    success_url = reverse_lazy("books:index")
    template_name = "users/auth/login.html"


def user_logout(request):
    logout(request)
    return redirect(reverse_lazy("books:index"))


@login_required
def profile(request):
    """
    Profile page view
    Processing update user
    Output update form and latest 20 comment by user.
    """
    profile_form = UserUpdateForm(instance=request.user)
    book_create_form = BookCreateForm()
    if request.method == "POST":
        if "update_profile" in request.POST:
            logger.info(f"Start updating profile by {request.user}")
            profile_form = UserUpdateForm(
                request.POST,
                request.FILES,
                instance=request.user
            )
            if profile_form.is_valid():
                profile_form.save()
                logger.info(f"Profile updated successfully")
                return redirect(reverse_lazy("users:profile"))
        elif "add_book" in request.POST:
            logger.info(f"Start creating book by {request.user} "
                        f"with data={request.POST}, {request.FILES}")
            book_create_form = BookCreateForm(
                request.POST,
                request.FILES
            )
            if book_create_form.is_valid():
                book = book_create_form.save(request.user)
                return redirect(
                    reverse_lazy(
                        "books:book_detail",
                        kwargs={"id": book.id}
                    )
                )
            else:
                logger.info(f"Error creating book, form is not valid, data={request.POST}")
                book_create_form = BookCreateForm(request.POST, request.FILES)
    latest_comments = comment_service.get_latest_comments(
        latest_count=20,
        author=request.user
    )
    context = {
        "user": request.user,
        "form_profile_update": profile_form,
        "book_create_form": book_create_form,
        "S3_DIR_USER_IMAGES_URL": S3_DIR_USER_IMAGES_URL,
        "S3_DIR_BOOK_COVERS_URL": S3_DIR_BOOK_COVERS_URL,
        "latest_comments": latest_comments
    }
    return render(request, "users/profile.html", context)


@login_required
def profile_comments(request):
    """
    All comments by user page view
    Output all user comments from new to old.
    """
    q = request.GET.get("q")
    if q:
        user_comments = comment_service.search_comments(author=request.user, q=q)
    else:
        user_comments = comment_service.comments_by_user(user=request.user)
    page_obj = paginator(request, user_comments)
    context = {
        "user": request.user,
        "S3_DIR_BOOK_COVERS_URL": S3_DIR_BOOK_COVERS_URL,
        "page_obj": page_obj,
    }
    return render(request, "users/comments.html", context)
