# Generated by Django 4.1.11 on 2023-11-21 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codeia", "0011_project_message_failed"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="short_sha",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="asset",
            name="url_commit",
            field=models.TextField(blank=True, default=""),
        ),
    ]
