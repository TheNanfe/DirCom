# Generated by Django 4.1.1 on 2022-11-02 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_persona_profile_picture"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["-date_joined"], "verbose_name": "usuario"},
        ),
    ]
