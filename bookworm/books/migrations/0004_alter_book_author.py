# Generated by Django 5.1 on 2024-09-19 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_alter_book_options_alter_book_publication_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
