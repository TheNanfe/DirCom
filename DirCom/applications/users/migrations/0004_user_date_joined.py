# Generated by Django 4.1.1 on 2022-09-11 22:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_user_id_alter_user_persona"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="date_joined",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
