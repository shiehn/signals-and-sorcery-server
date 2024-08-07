# Generated by Django 5.0.3 on 2024-04-30 18:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game_models", "0017_connection_connection_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameMap",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("level", models.IntegerField()),
                ("description", models.TextField()),
                ("map_graph", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
