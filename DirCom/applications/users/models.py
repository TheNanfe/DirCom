from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class Persona(models.Model):
    """
        Clase para generar mi modelo de Persona que es el modelo
        previo a crear un usuario, en este modelo se guardan todos
        los datos personales
    """
    DEPENDENCIES_CHOICES = (
        ("1", "Rectorado - Gabinete"),
        ("2", "Vice Rectorado"),
        ("3", "Rectorado - Secretaria General"),
        ("4", "Rectorado - Asesoría Jurídica"),
        ("5", "Rectorado - Auditoría General"),
        ("6", "Rectorado - DGA"),
        ("7", "Rectorado - DGAyF"),
        ("8", "Rectorado - DGEU"),
        ("9", "Rectorado - DGICT"),
        ("10", "Rectorado - DGGyTH"),
        ("11", "Rectorado - DGOTI"),
        ("12", "Rectorado - DGPD"),
        ("13", "Rectorado - DGP"),
        ("14", "Rectorado - DGPRI"),
        ("15","CNC - UNA"),
        ("16","CNEA - UNA"),
        ("17","CEMIT - UNA"),
        ("18","CETTRI - UNA"),
        ("19","IICS - UNA"),
        ("20","Biblioteca Central"),
        ("21", "INCUNA"),
        ("22", "UA - FDCS"),
        ("23", "UA - FCM"),
        ("24", "UA - FI"),
        ("25", "UA - FCE"),
        ("26", "UA - FO"),
        ("27", "UA - FCQ"),
        ("28", "UA - FCA"),
        ("29", "UA - FF"),
        ("30", "UA - FCV"),
        ("31", "UA - FADA"),
        ("32", "UA - FP"),
        ("33", "UA - FACEN"),
        ("34", "UA - FENOB"),
        ("35", "UA - FACSO"),
    )

    VINC_CHOICES = (("1", "Contratado"), ("2", "Permanente"),)

    gov_id = models.CharField("documento de identidad", max_length=50, unique=True)
    profile_picture = models.ImageField(
        "foto de perfil", upload_to="profiles", blank=True, null=True
    ) 
    email = models.EmailField("correo electrónico", max_length=254, unique=True) 
    first_name = models.CharField("nombres", blank=True, null=True, max_length=150)
    last_name = models.CharField("apellidos", blank=True, null=True, max_length=150)
    city = models.CharField("ciudad", blank=True, null=True,  max_length=30)
    phone = models.CharField("número de teléfono", blank=True, null=True, max_length=30)
    dependency = models.CharField("dependencia", blank=True, null=True, choices=DEPENDENCIES_CHOICES, max_length=2)
    vinc_type = models.CharField("tipo de vinculación", blank=True, null=True, choices=VINC_CHOICES, max_length=1)

    class Meta:
        verbose_name = "persona"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class User(AbstractBaseUser, PermissionsMixin):
    """ 
        Clase para generar mi modelo personalizado de usuarios
        AbstractBaseUser es un modelo de Django que ya trae integradas
        las funcionalidades de autenticación y manejo de sesiones
        Los campos que AbstractBaseUser ya trae predefinidos son:
        -id
        -password
        -is_superuser
    """
    ROLE_CHOICES = (
        (1, "Director"),
        (2, "Analista"),
        (3, "Cliente"),
        (4, "Técnico"),
    )

    username = models.CharField("nombre de usuario", max_length=50, unique=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, primary_key=True)
    role = models.PositiveSmallIntegerField("rol", choices=ROLE_CHOICES, default=ROLE_CHOICES[2][0])
    is_staff = models.BooleanField("staff", default=False)
    is_active = models.BooleanField("activo", default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # convierte el campo username en obligatorio por default
    USERNAME_FIELD = "username"

    # para que la terminal nos pida estos datos al crear un superuser
    REQUIRED_FIELDS = ['persona']

    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        ordering = ["-date_joined"]
