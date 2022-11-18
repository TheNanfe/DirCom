from django import template
from .models import Notification

register = template.Library()


@register.filter(name="notifications_number")
def get_notifications(user_pk):
    notifications = Notification.objects.filter(user_id=user_pk, status="PENDING")
    return notifications.__len__()
