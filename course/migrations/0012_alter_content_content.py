# Generated by Django 5.0.6 on 2024-06-21 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0011_alter_content_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="content",
            field=models.TextField(),
        ),
    ]
