# Generated by Django 5.1 on 2024-10-06 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=15, unique=True, verbose_name="username"),
        ),
    ]
