from django.db.models.signals import post_save

from .models import Ticket 

def clean_rejection_message(sender, instance, **kwargs):
    if instance.status != 4:
        sender.objects.filter(pk=instance.id).update(rejection_message="")

post_save.connect(clean_rejection_message, sender=Ticket, dispatch_uid="verify_rejection_message")