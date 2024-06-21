# Generated by Django 5.0.6 on 2024-06-21 06:16

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("iam", "0002_appuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appuser",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and _ only.",
                max_length=150,
                unique=True,
                validators=[
                    django.contrib.auth.validators.UnicodeUsernameValidator(
                        regex="^[a-zA-Z0-9_]+$"
                    )
                ],
                verbose_name="username",
            ),
        ),
    ]