from django.db import models
from applications.users.models import User


class Category(models.Model):
    title = models.CharField("título de la categoría", max_length=50)

    class Meta:
        verbose_name = "categoría"

    def __str__(self):
        return f"{self.title}"


class Ticket(models.Model):
    STATUS_CHOICES = (
        (1, "Pendiente"),
        (2, "En curso"),
        (3, "Finalizado"),
        (4, "Rechazado"),
    )

    URGENCY_CHOICES = (
        (1, "Urgente"),
        (2, "Alta"),
        (3, "Media"),
        (4, "Baja"),
    )

    user = models.ForeignKey(
        User,
        verbose_name="autor",
        related_name="user_tickets",
        on_delete=models.CASCADE,
    )
    agent = models.ForeignKey(
        User,
        verbose_name="agente",
        related_name="agent_tickets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    email = models.EmailField("correo electrónico", max_length=254)
    title = models.CharField("título", max_length=150)
    content = models.TextField("contenido")
    file = models.ImageField(
        "archivo adjunto", upload_to="files", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, verbose_name="categoría", on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(
        "estado", choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    urgency = models.PositiveSmallIntegerField(
        "urgencia", choices=URGENCY_CHOICES, default=URGENCY_CHOICES[2][0]
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("último cambio", auto_now=True)

    class Meta:
        verbose_name = "ticket"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id}: {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="autor",
        related_name="user_comments",
        on_delete=models.CASCADE,
    )
    ticket = models.ForeignKey(
        Ticket,
        verbose_name="ticket",
        related_name="ticket_comments",
        on_delete=models.CASCADE,
    )
    content = models.TextField("contenido")
    file = models.ImageField(
        "archivo adjunto", upload_to="files", blank=True, null=True
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "comentario"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} - {self.user} - Ticket: #{self.ticket.id}"