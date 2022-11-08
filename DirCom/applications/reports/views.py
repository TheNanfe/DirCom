import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods

from .report import TicketReport


class ReportsIndex(LoginRequiredMixin, TemplateView):
    """ El index de reportes, en donde se listan los reportes disponibles """

    template_name = "reports/reports_index.html"
    login_url = reverse_lazy("users_app:login")


@require_http_methods(["GET"])
def tickets_reports(request):
    """ Reporte de tickets por fechas """

    if not request.user.is_authenticated:
        # si el cliente no esta logeado se le lleva a la pantalla de login
        return HttpResponseRedirect(reverse_lazy("users_app:login"))

    if request.method == "GET":
        data = request.GET
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        ticket_report = TicketReport()
        try:
            if start_date is not None and end_date is not None:
                # se obtiene el reporte en base a las fechas filtradas
                ticket_report.report_by_dates(start_date, end_date)

            # se crea el contexto para pasarlo al template
            context = {
                "pending": json.dumps(ticket_report.pending_per_date),
                "on_course": json.dumps(ticket_report.on_course_per_date),
                "done": json.dumps(ticket_report.done_per_date),
                "rejected": json.dumps(ticket_report.rejected_per_date),
                "dates": json.dumps(ticket_report.dates),
                "total_per_date": json.dumps(ticket_report.total_per_date),
                "has_content": ticket_report.has_content,
                "dates_amount": len(ticket_report.dates),
                "start_date": ticket_report.format_dates(start_date),
                "end_date": ticket_report.format_dates(end_date),
                "total_tickets": ticket_report.total_tickets
            }
            # TODO: Aun hay datos para el reporte que no se estan utilizando. Crear una tabla para mostrarlos
            # TODO: Corregir el placeholder de los filtros de fechas del template
            return render(request, "reports/tickets_reports.html", context)

        except Exception as e:
            print("Exception has occurred! --> ", e)
            return HttpResponseRedirect(reverse_lazy("reports_app:reports_index"))
