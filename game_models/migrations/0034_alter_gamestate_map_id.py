# Generated by Django 5.0.3 on 2024-06-11 22:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game_models", "0033_alter_gamestate_environment_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gamestate",
            name="map_id",
            field=models.UUIDField(blank=True, null=True),
        ),
    ]