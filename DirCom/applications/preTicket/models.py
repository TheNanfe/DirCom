from django.db import models


# Create your models here.
class PreTicket(models.Model):
    pre_ticket_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mail = models.EmailField
    status = models.CharField(max_length=30)
    subject = models.CharField(max_length=150)
    form_type = models.CharField(max_length=50)
    text_content = models.TextField

    def __str__(self):
        self.first_name + self.last_name + self.mail
