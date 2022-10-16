from django.db import models
from applications.users.models import User


class Category(models.Model):
    title = models.CharField("título de la categoría", max_length=50)

    class Meta:
        verbose_name = "categoría"


class Comment(models.Model):
    content = models.TextField("contenido")
    file = models.ImageField("archivo adjunto", upload_to="files", blank=True, null=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "comentario"


class Ticket(models.Model):
    STATUS_CHOICES = (
        (1, "Pendiente"),
        (2, "Aprobado"),
        (3, "En curso"),
        (4, "Finalizado"),
    )

    URGENCY_CHOICES = (
        (1, "Urgente"),
        (2, "Alta"),
        (3, "Media"),
        (4, "Baja"),
    )

    user = models.ForeignKey(User, verbose_name="autor", related_name="user_tickets", on_delete=models.CASCADE)
    agent = models.ForeignKey(User, verbose_name="agente", related_name="agent_tickets", on_delete=models.CASCADE, blank=True, null=True)
    comments = models.ManyToManyField(Comment, related_name="comments")
    email = models.EmailField("correo electrónico", max_length=254) 
    title = models.CharField("título", max_length=150)
    content = models.TextField("contenido")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField("estado", choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    urgency = models.PositiveSmallIntegerField("urgencia", choices=URGENCY_CHOICES, default=URGENCY_CHOICES[2][0])
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("último cambio", auto_now=True)

    class Meta:
        verbose_name = "ticket"
