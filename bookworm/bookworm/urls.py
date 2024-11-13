from django.contrib import admin
from django.urls import path, include

from bookworm.admin import bookworm_admin_site


handler404 = "core.views.page_not_found"
handler403 = "core.views.csrf_failure"

urlpatterns = [
    path("", include("books.urls", namespace="books")),
    path("feedback/", include("feedback.urls", namespace="feedback")),
    path("users/", include("users.urls", namespace="users")),
    path("users/", include("django.contrib.auth.urls")),
    path("admin/", bookworm_admin_site.urls),
    path("tinymce/", include("tinymce.urls"))
]
