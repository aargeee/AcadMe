# Generated by Django 5.0.6 on 2024-06-21 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0006_alter_chapter_options_alter_content_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chapter",
            name="isLastChapter",
        ),
        migrations.RemoveField(
            model_name="content",
            name="isLastContent",
        ),
    ]