# Generated by Django 4.1.1 on 2022-10-23 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="persona",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="profiles",
                verbose_name="foto de perfil",
            ),
        ),
    ]
