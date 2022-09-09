from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    """
        este método sobreescribe la manera en que nuestro modelo
        de usuarios crea los nuevos usuarios
        es un método privado de la clase BaseUserManager por eso
        el nombre empieza con _
    """
    def _create_user(
        self,
        username,
        gov_id,
        email,
        password,
        is_staff,
        is_superuser,
        **extra_fields
    ):
        user = self.model(
            username=username,
            email=email,
            gov_id=gov_id,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    """
        este es un método público que sirve para crear usuarios normales
        no administradores, desde el frente de la aplicación, este es el 
        método que usamos para crear los usuarios en el registro de la página web
    """
    def create_user(self, username, email, gov_id, password=None, **extra_fields):
        self._create_user(
            username, email, gov_id, password, False, False, **extra_fields
        )

    """
        este es un método público que permite crear super usuarios, es decir,
        administradores con todos los permisos. Podemos crear usuarios desde
        la línea de comandos ejecutando python manage.py createsuperuser
    """
    def create_superuser(
        self, username, email, gov_id, password=None, **extra_fields
    ):
        return self._create_user(
            username, email, gov_id, password, True, True, **extra_fields
        )