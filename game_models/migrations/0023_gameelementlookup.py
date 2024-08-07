# Generated by Django 5.0.3 on 2024-05-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game_models", "0022_gamestate_environment_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameElementLookup",
            fields=[
                ("element_id", models.UUIDField(primary_key=True, serialize=False)),
                ("user_id", models.UUIDField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
