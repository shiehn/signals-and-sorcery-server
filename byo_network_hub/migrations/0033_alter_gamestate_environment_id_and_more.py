# Generated by Django 5.0.3 on 2024-06-08 04:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("byo_network_hub", "0032_gamemapstate_aesthetic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gamestate",
            name="environment_id",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="gamestate",
            name="environment_img",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
