from django.contrib import admin

from bookworm.admin import bookworm_admin_site
from feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "theme",
        "author",
        "text",
        "created_at",
    )
    search_fields = ("theme", "text",)
    list_filter = ("theme",)
    empty_value_display = "Пусто"


bookworm_admin_site.register(Feedback, FeedbackAdmin)
