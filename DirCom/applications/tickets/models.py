from django.db import models
from applications.users.models import User


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

    CATEGORIES = (
        (None, "---------"),
        ("PRENSA", "Prensa y Redacción"),
        ("AUDIOVISUAL", "Audiovisual"),
        ("DISENHO", "Diseño Grafico"),
        ("WEB", "Web"),
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
    category = models.CharField("categoria", max_length=50, choices=CATEGORIES, default="")
    status = models.PositiveSmallIntegerField(
        "estado", choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    urgency = models.PositiveSmallIntegerField(
        "urgencia", choices=URGENCY_CHOICES, default=URGENCY_CHOICES[2][0]
    )
    rejection_message = models.TextField("motivo del rechazo", blank=True, null=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("último cambio", auto_now=True)
    sub_category = models.CharField("subcategoria", null=True, max_length=5000)

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