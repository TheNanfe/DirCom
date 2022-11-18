from .models import Notification
from ..users.models import User


def create_notification(notification_type, **kwargs):
    notification_created = False
    try:
        if notification_type == "comment_creation":
            notification_created = comment_creation(notification_type,
                                                    kwargs["ticket_id"],
                                                    kwargs["user_id"],
                                                    kwargs["agent_id"],
                                                    kwargs["current_user"])

        if notification_type == "ticket_assignment":
            notification_created = ticket_assignment(notification_type,
                                                     kwargs["ticket_id"],
                                                     kwargs["agent_id"],
                                                     kwargs["current_agent"],
                                                     kwargs["ticket_title"])

        if notification_type == "created_ticket":
            notification_created = created_ticket(notification_type,
                                                  kwargs["ticket_id"],
                                                  kwargs["ticket_title"],
                                                  kwargs["user_id"])

        if notification_type == "reject_ticket":
            notification_created = reject_ticket(notification_type,
                                                 kwargs["ticket_id"],
                                                 kwargs["ticket_title"],
                                                 kwargs["user_id"])

        if notification_type == "approve_ticket":
            notification_created = approve_ticket(notification_type,
                                                  kwargs["ticket_id"],
                                                  kwargs["ticket_title"],
                                                  kwargs["user_id"])

        if notification_created:
            print("Notificacion creada con exito!")
        else:
            print("La notificacion no ha sido creada...")
    except Exception as e:
        raise e


def comment_creation(notification_type, ticket_id, user_id, agent_id, current_user):
    notification_created = False
    message = "Nuevo Comentario: Ticket #" + str(ticket_id)
    try:
        # notificacion para el agente
        if agent_id != "" and agent_id != current_user:
            Notification.objects.create(
                url_args=ticket_id,
                message=message,
                user_id=agent_id,
                notification_type=notification_type
            )
            notification_created = True
        # notificacion para el cliente
        if user_id != current_user:
            Notification.objects.create(
                url_args=ticket_id,
                message=message,
                user_id=user_id,
                notification_type=notification_type
            )
            notification_created = True

        return notification_created
    except Exception as e:
        raise e


def ticket_assignment(notification_type, ticket_id, agent_id, current_agent, ticket_title):
    message = "Ticket #" + str(ticket_id) + " Asignado: " + ticket_title
    notification_created = False
    try:
        if agent_id != "" and agent_id != current_agent:
            Notification.objects.create(
                url_args=ticket_id,
                message=message,
                user_id=agent_id,
                notification_type=notification_type
            )
            notification_created = True

        return notification_created

    except Exception as e:
        raise e


def created_ticket(notification_type, ticket_id, ticket_title, user_id):
    message = "Ticket #" + str(ticket_id) + " Creado! : " + ticket_title
    try:
        Notification.objects.create(
            url_args=ticket_id,
            message=message,
            user_id=user_id,
            notification_type=notification_type
        )

        return True
    except Exception as e:
        raise e


def reject_ticket(notification_type, ticket_id, ticket_title, user_id):
    message = "Ticket #" + str(ticket_id) + " Rechazado. : " + ticket_title
    try:
        Notification.objects.create(
            url_args=ticket_id,
            message=message,
            user_id=user_id,
            notification_type=notification_type
        )

        admin_list = User.objects.filter(role=1).values("pk")
        for admin in admin_list:
            Notification.objects.create(
                url_args=ticket_id,
                message=message,
                user_id=admin["pk"],
                notification_type=notification_type
            )

        return True
    except Exception as e:
        raise e


def approve_ticket(notification_type, ticket_id, ticket_title, user_id):
    message = "Ticket #" + str(ticket_id) + " Aprobado! : " + ticket_title
    try:
        Notification.objects.create(
            url_args=ticket_id,
            message=message,
            user_id=user_id,
            notification_type=notification_type
        )

        admin_list = User.objects.filter(role=1).values("pk")
        for admin in admin_list:
            Notification.objects.create(
                url_args=ticket_id,
                message=message,
                user_id=admin["pk"],
                notification_type=notification_type
            )

        return True
    except Exception as e:
        raise e
