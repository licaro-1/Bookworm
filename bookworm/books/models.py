from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from tinymce.models import HTMLField

User = get_user_model()


def validate_text_length(text: str):
    if len(text) < 80:
        raise ValidationError("Текст слишком короткий (минимум 80 символов)")


class Book(models.Model):
    creator = models.ForeignKey(
        User,
        default=None,
        blank=True,
        null=True,
        verbose_name="Создатель",
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=300,
        unique=True,
        blank=False,
        verbose_name="Название",
    )
    author = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Автор",
    )
    publication_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Год публикации",
    )
    description = models.CharField(
        max_length=4000,
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    image = models.CharField(
        max_length=400,
        blank=False,
        verbose_name="Изображение",
    )
    views = models.IntegerField(
        default=0,
        verbose_name="Просмотры"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    @property
    def rating_average(self):
        comments = self.comments.all()
        if comments:
            rating = round(sum(c.rating for c in comments) / len(comments), 2)
            return rating
        return 0

    @property
    def rating_count(self):
        return self.comments.count()

    def __str__(self):
        return f"Book({self.title}, {self.publication_year})"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Книга",
        verbose_name_plural = "Книги"


class Comment(models.Model):
    RAITING_CHOICES = [
        (1, "1 - Зря потратил время"),
        (2, "2 - Не стоит того"),
        (3, "3 - Средняя, могло быть лучше"),
        (4, "4 - Хорошая, стоит почитать"),
        (5, "5 - Отличная, оправдала ожидания"),
    ]
    book = models.ForeignKey(
        Book,
        null=False,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Книга"
    )
    author = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name="commented",
        verbose_name="Автор",
    )
    text = HTMLField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    rating = models.IntegerField(
        null=False,
        default=1,
        verbose_name="Рейтинг",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RAITING_CHOICES
    )
    recommended = models.BooleanField(default=False, verbose_name="Рекомендую")
    is_edited = models.BooleanField(
        default=False,
        verbose_name="Редактировался"
    )

    def __str__(self):
        return f"Comment(<{self.id=}, {self.author=}, {self.book=}>)"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-created_at",)
