# Generated by Django 5.0.3 on 2024-04-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game_models", "0015_remove_connectionstatus_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="connectionstatus",
            name="loaded",
            field=models.BooleanField(default=False),
        ),
    ]
