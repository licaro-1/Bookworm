# Generated by Django 5.1.2 on 2024-11-09 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0014_alter_comment_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="description",
            field=models.CharField(
                blank=True, max_length=3000, null=True, verbose_name="Описание"
            ),
        ),
    ]
