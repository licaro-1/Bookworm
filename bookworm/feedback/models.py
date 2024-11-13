import uuid

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Feedback(models.Model):
    """Feedback model."""
    THEME_CHOICES = [
        ("collaboration", "Сотрудничество"),
        ("suggestion", "Предложение по улучшению"),
        ("error", "Ошибка в работе сайта"),
        ("other", "Другое"),
    ]
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    theme = models.CharField(
        choices=THEME_CHOICES,
        default="suggestion",
        max_length=180,
        verbose_name="Тема"
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"Feedback({self.theme}, {self.text[:20]}...)"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ("-created_at",)
