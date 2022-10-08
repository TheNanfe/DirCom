from django.db import models
from datetime import *


# Create your models here.
class PreTicket(models.Model):
    pre_ticket_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mail = models.CharField(max_length=150, null=False, default="")
    status = models.CharField(max_length=30)
    subject = models.CharField(max_length=150)
    form_type = models.CharField(max_length=50)
    text_content = models.CharField(max_length=3000, null=False, default="")
    creation_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return str(self.first_name) + self.last_name + self.mail


class UploadFiles(models.Model):
    id_file = models.AutoField(primary_key=True)
    id_pre_ticket = models.ForeignKey(PreTicket, on_delete=models.CASCADE)
    # TODO: Agregar el campo de fk del ticket(aceptado)
    # id_ticket = id_pre_ticket = models.ForeignKey(Ticket)
    file_path = models.CharField(max_length=300, null=False, default="")
    file_name = models.CharField(max_length=100)


