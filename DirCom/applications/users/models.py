from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ 
        Clase para generar mi modelo personalizado de usuarios
        AbstractBaseUser es un modelo de Django que ya trae integradas
        las funcionalidades de autenticación y manejo de sesiones
        Los campos que AbstractBaseUser ya trae predefinidos son:
        -id
        -password
        -is_admin
    """

    VINC_CHOICES = (("1", "Contratado"), ("2", "Permanente"),)

    # campos obligatorios
    username = models.CharField("nombre de usuario", max_length=50, unique=True) 
    gov_id = models.CharField("documento de identidad", max_length=50, unique=True) 
    email = models.EmailField("correo electrónico", max_length=254, unique=True) 
    # campos extras
    first_name = models.CharField("nombres", blank=True, null=True, max_length=150)
    last_name = models.CharField("apellidos", blank=True, null=True, max_length=150)
    city = models.CharField("ciudad", blank=True, null=True,  max_length=30)
    phone = models.CharField("número de teléfono", blank=True, null=True, max_length=30)
    area = models.CharField("dependencia", blank=True, null=True, max_length=150)
    vinc_type = models.CharField("tipo de vinculación", blank=True, null=True, choices=VINC_CHOICES, max_length=1)
    is_staff = models.BooleanField("staff", default=False)

    # convierte el campo username en obligatorio por default
    USERNAME_FIELD = "username"

    # para que la terminal nos pida estos datos al crear un superuser
    REQUIRED_FIELDS = ['email', 'gov_id']

    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
