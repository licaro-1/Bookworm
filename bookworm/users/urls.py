from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path

from users import views


app_name = "users"


urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("profile/comments/", views.profile_comments, name="profile_comments"),
    path("login/", views.Login.as_view(), name="login"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="users/auth/password_change.html",
        ),
        name="password_change"
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/auth/password_reset_form.html",
        ),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="users/auth/password_reset_done.html",
        ),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="users/auth/password_reset_complete.html"
        ),
        name="password_reset_complete"
    )
]
