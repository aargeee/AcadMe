# Generated by Django 5.0.6 on 2024-06-23 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]