# Generated by Django 5.0.1 on 2024-03-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game_models", "0012_remotesource"),
    ]

    operations = [
        migrations.AddField(
            model_name="remotesource",
            name="colab_url",
            field=models.CharField(max_length=1500, null=True),
        ),
    ]
