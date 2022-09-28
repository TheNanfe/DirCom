from django.db import models
#from DirCom.applications.preTicket.models import PreTicket


# Create your models here.


class UploadFiles(models.Model):
    id_file = models.AutoField(primary_key=True)
    #id_pre_ticket = models.ForeignKey(PreTicket)
    # TODO: Agregar el campo de fk del ticket(aceptado)
    # id_ticket = id_pre_ticket = models.ForeignKey(Ticket)
    file_path = models.TextField
    file_name = models.CharField(max_length=100)
