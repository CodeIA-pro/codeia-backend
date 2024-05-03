# Generated by Django 4.1.11 on 2024-05-03 06:24

import codeia.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("codeia", "0022_user_user_github"),
    ]

    operations = [
        migrations.CreateModel(
            name="Star",
            fields=[
                ("value", models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                "managed": False,
            },
        ),
        migrations.AddField(
            model_name="asset",
            name="stars",
            field=djongo.models.fields.ArrayField(
                default=list, model_container=codeia.models.Star, null=True
            ),
        ),
    ]
