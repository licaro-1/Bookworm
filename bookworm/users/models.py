from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from bookworm.settings import DEFAULT_USER_AVATAR_IMG


class User(AbstractUser):
    """User model."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = [
        (ADMIN, "Administrator"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
    ]

    email = models.EmailField(
        verbose_name="Почта",
        unique=True,
        blank=False
    )
    username = models.CharField(
        verbose_name="Юзернейм",
        max_length=15,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=10,
        blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=10,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name="Активный аккаунт",
        default=True
    )
    date_joined = models.DateTimeField(
        verbose_name="Дата регистрации",
        default=timezone.now
    )
    last_login = models.DateTimeField(
        verbose_name="Последний вход",
        default=timezone.now
    )
    avatar = models.CharField(
        "Аватар",
        max_length=200,
        blank=True,
        null=False,
        default=DEFAULT_USER_AVATAR_IMG
    )
    role = models.CharField(
        _("Роль"),
        max_length=30,
        choices=ROLES,
        default=USER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    @property
    def is_admin(self):
        """Checking user is admin."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Checking user is moderator."""
        return self.role == self.MODERATOR

    def __str__(self):
        return f"User({self.id}, {self.email})"

    class Meta:
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-date_joined",)
