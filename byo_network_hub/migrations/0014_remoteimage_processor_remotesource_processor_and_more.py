# Generated by Django 5.0.3 on 2024-04-02 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("byo_network_hub", "0013_remotesource_colab_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="remoteimage",
            name="processor",
            field=models.CharField(
                choices=[("cpu", "CPU"), ("gpu", "GPU")], default="cpu", max_length=25
            ),
        ),
        migrations.AddField(
            model_name="remotesource",
            name="processor",
            field=models.CharField(
                choices=[("cpu", "CPU"), ("gpu", "GPU")], default="cpu", max_length=25
            ),
        ),
        migrations.AlterField(
            model_name="remoteimage",
            name="remote_category",
            field=models.CharField(
                choices=[
                    ("audio", "AUDIO"),
                    ("video", "VIDEO"),
                    ("image", "IMAGE"),
                    ("text", "TEXT"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="remotesource",
            name="remote_category",
            field=models.CharField(
                choices=[
                    ("audio", "AUDIO"),
                    ("video", "VIDEO"),
                    ("image", "IMAGE"),
                    ("text", "TEXT"),
                ],
                max_length=100,
            ),
        ),
    ]
