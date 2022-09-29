from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .forms import FileHandlerForm, UploadFileHandlerForm, PreTicketForm
from .utils import *
from django.contrib import messages
from .models import PreTicket, UploadFiles

# Create your views here.


@require_http_methods(["GET", "POST"])
def pre_ticket_creation_form(request):
    if request.method == "GET":
        return HttpResponse(render(request, template_name="preTicket/form_creation.html"))
    if request.method == "POST":
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        mail = data.get("mail")
        subject = data.get("subject")
        status = data.get("status")
        form_type = data.get("form_type")
        text_content = data.get("text_content")

        form = FileHandlerForm(request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist("files"):
                file_path = handle_uploaded_file(file)
                if file_path is not None:
                    pre_ticket = PreTicket(first_name=first_name, last_name=last_name, mail=mail, subject=subject,
                                           status=status, form_type=form_type, text_content=text_content)
                    pre_ticket.save()
                    upload_file = UploadFiles(file_name=file.name, id_pre_ticket=pre_ticket,
                                              file_path=file_path)
                    upload_file.save()
            messages.info(request, "La peticion ha sido creada con exito!")
            return HttpResponse(render(request, template_name="preTicket/form_creation.html"))

    messages.error(request, "Ha ocurrido un error al tratar de crear la solicitud")
    return HttpResponse(render(request, template_name="preTicket/form_creation.html"))
