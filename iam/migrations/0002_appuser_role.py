# Generated by Django 5.0.6 on 2024-06-21 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("iam", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("ADMIN", "ADMIN"),
                    ("TUTOR", "TUTOR"),
                    ("LEARNER", "LEARNER"),
                ],
                default="ADMIN",
                max_length=10,
            ),
        ),
    ]