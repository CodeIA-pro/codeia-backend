# Generated by Django 4.1.11 on 2023-11-20 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codeia", "0010_project_urls"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="message_failed",
            field=models.TextField(blank=True, default=""),
        ),
    ]
