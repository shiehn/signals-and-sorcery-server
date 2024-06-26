# Generated by Django 5.0.3 on 2024-05-30 22:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("byo_network_hub", "0028_gameupdatequeue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gameupdatequeue",
            name="status",
            field=models.CharField(
                choices=[
                    ("queued", "Queued"),
                    ("started", "Started"),
                    ("completed", "Completed"),
                    ("error", "Error"),
                ],
                default="queued",
                max_length=10,
            ),
        ),
    ]
