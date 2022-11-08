import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .report import TicketReport


# Create your views here.


class ReportsIndex(LoginRequiredMixin, TemplateView):
    template_name = "reports/reports_index.html"


@require_http_methods(["GET"])
def tickets_reports(request):
    data = request.GET
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    ticket_report = TicketReport()
    if start_date is not None and end_date is not None:
        ticket_report.report_by_dates(start_date, end_date)
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
    return render(request, "reports/tickets_reports.html", context)
