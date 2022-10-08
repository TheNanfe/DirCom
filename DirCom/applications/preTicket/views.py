from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from .forms import FileHandlerForm, UploadFileHandlerForm, PreTicketForm
from .utils import *
from django.contrib import messages
from .models import PreTicket, UploadFiles

# Constantes globales
NO_PRE_TICKET_MSG = "No existen Pre Tickets pendientes de procesar"


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
            pre_ticket = PreTicket(first_name=first_name, last_name=last_name, mail=mail, subject=subject,
                                   status=status, form_type=form_type, text_content=text_content)
            pre_ticket.save()
            for file in request.FILES.getlist("files"):
                file_path = handle_uploaded_file(file)
                if file_path is not None:
                    upload_file = UploadFiles(file_name=file.name, id_pre_ticket=pre_ticket,
                                              file_path=file_path)
                    upload_file.save()
            messages.info(request, "La peticion ha sido creada con exito!")
            return HttpResponse(render(request, template_name="preTicket/form_creation.html"))

    messages.error(request, "Ha ocurrido un error al tratar de crear la solicitud")
    return HttpResponse(render(request, template_name="preTicket/form_creation.html"))


@require_http_methods(["GET", "POST"])
def pre_ticket_status_change(request, pk=None):
    if request.method == "GET":
        pre_ticket_context = {}
        try:
            if pk is not None and pk != "":
                pre_ticket = PreTicket.objects.get(pk=pk)
                if pre_ticket.status != "pending":
                    messages.info(request, "Pre Ticker ya procesado")
                    return HttpResponseRedirect(reverse("pre_ticket_app:list_pre_tickets"))
            else:
                pre_ticket = PreTicket.objects.filter(status="pending")[0]
        except Exception as e:
            print(e)
            messages.info(request, NO_PRE_TICKET_MSG)
            return HttpResponseRedirect(reverse("pre_ticket_app:list_pre_tickets"))
        if pre_ticket is None:
            messages.info(request, NO_PRE_TICKET_MSG)
            return HttpResponseRedirect(reverse("pre_ticket_app:list_pre_tickets"))
        pre_ticket_context["pre_ticket_id"] = pre_ticket.pre_ticket_id
        pre_ticket_context["first_name"] = pre_ticket.first_name
        pre_ticket_context["last_name"] = pre_ticket.last_name
        pre_ticket_context["mail"] = pre_ticket.mail
        pre_ticket_context["subject"] = pre_ticket.subject
        pre_ticket_context["form_type"] = pre_ticket.form_type
        pre_ticket_context["content"] = pre_ticket.text_content
        return render(request, "preTicket/pre_ticket_status_change.html", pre_ticket_context)

    if request.method == "POST":
        data = request.POST
        pre_ticket_id = data.get("pre_ticket_id")
        pre_ticket_status = data.get("status")
        pre_ticket = PreTicket.objects.filter(pk=pre_ticket_id)
        pre_ticket.update(status=pre_ticket_status)
        return HttpResponseRedirect(reverse("pre_ticket_app:pre_ticket_status_change"))


@require_http_methods(["GET"])
def list_pre_tickets(request):
    pre_ticket_list = PreTicket.objects.filter(status="pending")
    context = {
        "pre_ticket_list": pre_ticket_list
    }
    return render(request, "preTicket/pre_ticket_list.html", context)

# TODO: Para cuando el Pre Ticket es rechazado, hay que crear un Pop-Up que pida el motivo del rechazo
