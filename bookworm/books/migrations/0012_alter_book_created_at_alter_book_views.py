# Generated by Django 5.1 on 2024-10-12 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0011_book_creator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата добавления"
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="views",
            field=models.IntegerField(default=0, verbose_name="Просмотры"),
        ),
    ]
