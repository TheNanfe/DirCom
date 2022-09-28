from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from files.forms import FileHandlerForm, UploadFileHandlerForm
from .forms import PreTicketForm
from .utils import *
from django.contrib import messages
from .models import PreTicket

# Create your views here.


@require_http_methods(["GET", "POST"])
def pre_ticket_creation_form(request):
    if request.method == "GET":
        return HttpResponse(render(request, template_name="preTicket/form_creation.html"))
    if request.method == "POST":
        form = FileHandlerForm(request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist("files"):
                successfully_saved = handle_uploaded_file(file)
                if successfully_saved:
                    pre_ticket = PreTicketForm(request.POST)
                    if pre_ticket.is_valid():
                        pre_ticket.save()
            messages.info(request, "La peticion ha sido creada con exito!")
            return HttpResponse(render(request, template_name="preTicket/form_creation.html"))

    messages.error(request, "ha ocurrido un error")
    return HttpResponse(render(request, template_name="preTicket/form_creation.html"))
