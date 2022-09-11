# Generated by Django 4.1.1 on 2022-09-11 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Persona",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gov_id",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        verbose_name="documento de identidad",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="correo electrónico"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="nombres"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="apellidos"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="ciudad"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=30,
                        null=True,
                        verbose_name="número de teléfono",
                    ),
                ),
                (
                    "area",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="dependencia",
                    ),
                ),
                (
                    "vinc_type",
                    models.CharField(
                        blank=True,
                        choices=[("1", "Contratado"), ("2", "Permanente")],
                        max_length=1,
                        null=True,
                        verbose_name="tipo de vinculación",
                    ),
                ),
            ],
            options={
                "verbose_name": "persona",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="nombre de usuario"
                    ),
                ),
                ("is_staff", models.BooleanField(default=False, verbose_name="staff")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "persona",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to="users.persona",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "usuario",
            },
        ),
    ]