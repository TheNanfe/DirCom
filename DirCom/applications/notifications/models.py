from django.db import models
from ..users.models import User


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, default=1)
    url_args = models.CharField(max_length=1000, null=False)
    message = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default="PENDING")
    notification_type = models.CharField(max_length=100)
    status_read = models.CharField(max_length=50, default="UNREAD")
    title = models.CharField(max_length=500, default="")
