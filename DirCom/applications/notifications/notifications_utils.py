from .models import Notification
from ..users.models import User
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse


def send_email_notification(subject, context, mail_to):
    """
    subject: asunto del email
    context: diccionario con {
        title: "titulo de la notificacion",
        content: "contenido de texto de la notificacion",
        url: "url a la que quieres dirigir al usuario al abrir el correo",
        action_text: "texto del boton en la plantilla del email"
    }
    mail_to: destinatario de la notificación

    EJEMPLO:
    send_email_notification("Ticket creado", {
        "title": "Gracias por crear un ticket en DirComCRM",
        "content": "Hemos recibido tu ticket, en las próximas horas un agente se pondrá en contacto contigo",
        "url":  settings.APP_DOMAIN
                    + reverse("tickets_app:detail", kwargs={"pk": kwargs["ticket_id"]}),
                    "action_text": "Ver mi ticket",
        "action_text": "Ver mi ticket"
    }, user.email)
    """
    html_content = render_to_string("core/email.html", context)
    text_content = striptags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, [mail_to])
    msg.attach_alternative(html_content, "text/html")
    print(mail_to)
    print(context)
    msg.send()


def create_notification(notification_type, **kwargs):
    notification_created = False
    try:
        if notification_type == "comment_creation":
            notification_created = comment_creation(
                notification_type,
                kwargs["ticket_id"],
                kwargs["user_id"],
                kwargs["agent_id"],
                kwargs["current_user"],
                kwargs["ticket_title"],
            )

        if notification_type == "ticket_assignment":
            notification_created = ticket_assignment(
                notification_type,
                kwargs["ticket_id"],
                kwargs["agent_id"],
                kwargs["current_agent"],
                kwargs["ticket_title"],
            )

            # enviar mail al agente
            send_email_notification(
                "Ticket creado",
                {
                    "title": "Gracias por crear un ticket en DirComCRM",
                    "content": "Hemos recibido tu ticket, en las próximas horas un agente se pondrá en contacto contigo",
                    "url": settings.APP_DOMAIN
                    + reverse("tickets_app:detail", kwargs={"pk": kwargs["ticket_id"]}),
                    "action_text": "Ver mi ticket",
                },
                User.objects.get(pk=kwargs["agent_id"]).persona.email,
            )

        if notification_type == "created_ticket":
            notification_created = created_ticket(
                notification_type,
                kwargs["ticket_id"],
                kwargs["ticket_title"],
                kwargs["user_id"],
            )

        if notification_type == "reject_ticket":
            notification_created = reject_ticket(
                notification_type,
                kwargs["ticket_id"],
                kwargs["ticket_title"],
                kwargs["user_id"],
                kwargs["current_admin"],
            )

        if notification_type == "approve_ticket":
            notification_created = approve_ticket(
                notification_type,
                kwargs["ticket_id"],
                kwargs["ticket_title"],
                kwargs["user_id"],
                kwargs["current_admin"],
            )

        if notification_created:
            print("Notificacion creada con exito!")
        else:
            print("La notificacion no ha sido creada...")
    except Exception as e:
        raise e


def comment_creation(
    notification_type, ticket_id, user_id, agent_id, current_user, ticket_title
):
    notification_created = False
    message = "Nuevo Comentario Ticket #" + str(ticket_id) + ": "
    try:
        # notificacion para el agente
        if agent_id != "" and agent_id != current_user:
            creation(ticket_id, message, agent_id, notification_type, ticket_title)
            notification_created = True
        # notificacion para el cliente
        if user_id != current_user:
            creation(ticket_id, message, user_id, notification_type, ticket_title)
            notification_created = True
        return notification_created
    except Exception as e:
        raise e


def ticket_assignment(
    notification_type, ticket_id, agent_id, current_agent, ticket_title
):
    message = "Ticket #" + str(ticket_id) + " Asignado: "
    notification_created = False
    try:
        if agent_id != "" and agent_id != current_agent:
            creation(ticket_id, message, agent_id, notification_type, ticket_title)
            notification_created = True
        return notification_created

    except Exception as e:
        raise e


def created_ticket(notification_type, ticket_id, ticket_title, user_id):
    message = "Ticket #" + str(ticket_id) + " Creado! : "
    try:
        creation(ticket_id, message, user_id, notification_type, ticket_title)
        return True
    except Exception as e:
        raise e


def reject_ticket(notification_type, ticket_id, ticket_title, user_id, current_admin):
    message = "Ticket #" + str(ticket_id) + " Rechazado : "
    try:
        creation(ticket_id, message, user_id, notification_type, ticket_title)
        admin_list = User.objects.filter(role=1).values("pk")
        for admin in admin_list:
            if admin["pk"] != current_admin:
                creation(
                    ticket_id, message, admin["pk"], notification_type, ticket_title
                )
        return True
    except Exception as e:
        raise e


def approve_ticket(notification_type, ticket_id, ticket_title, user_id, current_admin):
    message = "Ticket #" + str(ticket_id) + " Aprobado : "
    try:
        creation(ticket_id, message, user_id, notification_type, ticket_title)
        admin_list = User.objects.filter(role=1).values("pk")
        for admin in admin_list:
            if admin["pk"] != current_admin:
                creation(
                    ticket_id, message, admin["pk"], notification_type, ticket_title
                )
        return True
    except Exception as e:
        raise e


def creation(ticket_id, message, user_id, notification_type, ticket_title):
    Notification.objects.create(
        url_args=ticket_id,
        message=message,
        user_id=user_id,
        notification_type=notification_type,
        title=ticket_title,
    )


def get_notifications_for_user(user_notifications):
    notifications = {}
    notification_array = []
    for notification in user_notifications:
        notification_array.append(
            {
                "id": notification.id,
                "message": notification.message,
                "url_args": notification.url_args,
                "notification_type": notification.notification_type,
                "status_read": notification.status_read,
                "title": notification.title,
            }
        )
    notifications["notifications"] = notification_array
    return notifications
