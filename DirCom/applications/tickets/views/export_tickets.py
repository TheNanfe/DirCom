import csv
import io
import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import date, datetime, timedelta
from django.utils import formats

from applications.tickets.models import Ticket, Category
from applications.users.models import User


def export_tickets(request):
    agents = User.objects.filter(role=2)
    categories = Category.objects.all()
    today = datetime.today().strftime("%Y-%m-%d")
    context = {
        "agents": agents,
        "categories": categories,
        "today": today,
    }
    return render(request, "tickets/export.html", context)


# el siguiente método está en mantenimiento
def export_tickets_pdf(request):
    buf = io.BytesIO()
    my_canvas = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    content = my_canvas.beginText()
    content.setTextOrigin(inch, inch)
    content.setFont("Helvetica", 14)

    lines = []

    tickets = Ticket.objects.all()

    for ticket in tickets:
        lines.append(str(ticket.id))
        lines.append(ticket.title)
        lines.append(str(ticket.user.persona))
        lines.append(ticket.get_status_display())
        lines.append(str(ticket.agent))
        lines.append(ticket.content)
        lines.append(str(ticket.category))
        # lines.append(ticket.created_at)
        lines.append(" ")

    for line in lines:
        content.textLine(line)

    my_canvas.drawText(content)
    my_canvas.showPage()
    my_canvas.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="tickets.pdf")


def export_tickets_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=tickets.csv"

    writer = csv.writer(response)

    tickets = Ticket.objects.all()

    # filtros
    status = request.GET.get("status", "")
    agent = request.GET.get("agent", "")
    urgency = request.GET.get("urgency", "")
    category = request.GET.get("category", "")
    dateFrom = request.GET.get("from", "")
    dateTo = request.GET.get("to", "")

    if status:
        tickets = tickets.filter(status=status)
    if agent:
        agent = User.objects.get(username=agent)
        tickets = tickets.filter(agent=agent)
    if urgency:
        tickets = tickets.filter(urgency=urgency)
    if category:
        tickets = tickets.filter(category=category)
    if dateFrom:
        dateFrom = f"{dateFrom} 00:00"
        dateTo = f"{dateTo} 00:00" if dateTo else datetime.today()
        tickets = tickets.filter(created_at__range=(dateFrom, dateTo))

    # agregar los encabezados de las columnas
    writer.writerow(
        [
            "Autor",
            "Email",
            "Título",
            "Estado",
            "Urgencia",
            "Categoría",
            "Agente",
            "Fecha de creación",
            "Ver ticket",
            "Motivo de rechazo",
        ]
    )

    for ticket in tickets:
        writer.writerow(
            [
                str(ticket.user.persona),
                ticket.email,
                ticket.title,
                ticket.get_status_display(),
                ticket.get_urgency_display(),
                ticket.category.title,
                ticket.agent.persona if ticket.agent else "No asignado",
                ticket.created_at.strftime("%d-%m-%Y %H:%M"),
                request.build_absolute_uri(
                    reverse("tickets_app:detail", kwargs={"pk": ticket.id})
                ),
                ticket.rejection_message,
            ]
        )

    return response


def formatDate(d):
    return "Fecha_" + formats.date_format(d, "d_m_Y")


def tickets_reports(request):
    tickets = Ticket.objects.all()

    form_has_date_from = False
    if request.GET.get("from", ""):
        form_has_date_from = True

    form_has_date_to = False
    if request.GET.get("to", ""):
        form_has_date_to = True

    # filtros
    status = request.GET.get("status", "")
    agent = request.GET.get("agent", "")
    urgency = request.GET.get("urgency", "")
    category = request.GET.get("category", "")
    dateFrom = request.GET.get("from", datetime.today() - timedelta(days=7))
    dateTo = request.GET.get("to", datetime.today())

    if status:
        tickets = tickets.filter(status=status)
    if agent:
        agent = User.objects.get(username=agent)
        tickets = tickets.filter(agent=agent)
    if urgency:
        tickets = tickets.filter(urgency=urgency)
    if category:
        tickets = tickets.filter(category=category)
    if dateFrom:
        if form_has_date_from:
            dateFrom = f"{dateFrom} 00:00"
        if form_has_date_to:
            dateTo = f"{dateTo} 00:00" if dateTo else datetime.today()
        tickets = tickets.filter(created_at__range=(dateFrom, dateTo))

    result = {}
    if form_has_date_from:
        delta = datetime.strptime(dateTo, "%Y-%m-%d %H:%M") - datetime.strptime(
            dateFrom, "%Y-%m-%d %H:%M"
        )
    else:
        delta = dateTo - dateFrom

    for i in range(delta.days + 1):
        day = (
            datetime.strptime(dateFrom, "%Y-%m-%d %H:%M") + timedelta(days=i)
            if form_has_date_from
            else dateFrom + timedelta(days=i)
        )
        result[formatDate(day)] = 0
    for ticket in tickets:
        result[formatDate(ticket.created_at)] += 1

    agents = User.objects.filter(role=2)
    categories = Category.objects.all()
    today = datetime.today().strftime("%Y-%m-%d")
    default_from = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    context = {
        "result": json.dumps(result), 
        "today": today,
        "default_from": default_from,
        "agents": agents,
        "categories": categories
    }
    return render(request, "tickets/reports.html", context)
