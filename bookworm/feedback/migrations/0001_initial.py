# Generated by Django 5.1.2 on 2024-10-27 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "theme",
                    models.CharField(
                        choices=[
                            ("collaboration", "Сотрудничество"),
                            ("suggestion", "Предложение по улучшению"),
                            ("error", "Ошибка в работе сайта"),
                            ("question", "Вопрос"),
                            ("other", "Другое"),
                        ],
                        default="suggestion",
                        max_length=180,
                        verbose_name="Тема",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=2000, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Обращение",
                "verbose_name_plural": "Обращения",
                "ordering": ("-created_at",),
            },
        ),
    ]
