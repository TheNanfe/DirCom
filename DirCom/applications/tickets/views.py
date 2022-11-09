from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import datetime
import csv

from applications.users.models import User
from .models import Comment, Ticket, Category
from .forms import (
    AddTicketForm,
    AddCommentForm,
    AdminEditTicketForm,
    EditTicketForm,
    RejectionMessageForm,
)


class AllTicketsView(LoginRequiredMixin, ListView):
    template_name = "tickets/all.html"
    context_object_name = "tickets"
    paginate_by = 12
    login_url = reverse_lazy("users_app:login")

    def get_queryset(self):
        title = self.request.GET.get("title", "")
        status = self.request.GET.get("status", "")
        urgency = self.request.GET.get("urgency", "")
        # todos los tickets para el admin
        if self.request.user.role == 1:
            tickets = Ticket.objects.all()
        # solo tickets asignados al analista
        if self.request.user.role == 2:
            tickets = Ticket.objects.filter(agent=self.request.user).filter(
                ~Q(status=4)
            )
        # solo tickets propios para el cliente
        if self.request.user.role == 3:
            tickets = Ticket.objects.filter(user=self.request.user)
        if title:
            tickets = tickets.filter(title__icontains=title)
        if status:
            tickets = tickets.filter(status=status)
        if urgency:
            tickets = tickets.filter(urgency=urgency)
        return tickets

    def get_context_data(self, **kwargs):
        context = super(AllTicketsView, self).get_context_data(**kwargs)
        context["title"] = self.request.GET.get("title", "")
        context["status"] = self.request.GET.get("status", "")
        context["urgency"] = self.request.GET.get("urgency", "")
        return context


class DetailTicketView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "tickets/detail.html"
    context_object_name = "ticket"
    login_url = reverse_lazy("users_app:login")


class CreateTicketView(LoginRequiredMixin, FormView):
    form_class = AddTicketForm
    success_url = reverse_lazy("tickets_app:thanks")
    template_name = "tickets/create.html"
    login_url = reverse_lazy("users_app:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 3:
            return redirect("core_app:home")
        else:
            return super(CreateTicketView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        Ticket.objects.create(
            user=self.request.user,
            email=form.cleaned_data["email"],
            title=form.cleaned_data["title"],
            content=form.cleaned_data["content"],
            file=form.cleaned_data["file"],
            category=form.cleaned_data["category"],
        )
        return super().form_valid(form)


class AproveOrRejectTicketView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "tickets/aprove.html"
    context_object_name = "ticket"
    login_url = reverse_lazy("users_app:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(AproveOrRejectTicketView, self).dispatch(
                request, *args, **kwargs
            )


class AproveTicketView(LoginRequiredMixin, View):
    """vista para que el admin apruebe los tickets"""

    login_url = reverse_lazy("users_app:login")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", "default")
        ticket = Ticket.objects.get(pk=pk)
        ticket.status = 2
        ticket.save()
        return HttpResponseRedirect(reverse("tickets_app:edit", kwargs={"pk": pk}))

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(AproveTicketView, self).dispatch(
                request, *args, **kwargs
            )

class RejectTicketView(LoginRequiredMixin, View):
    """vista para que el admin rechace los tickets"""

    login_url = reverse_lazy("users_app:login")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", "default")
        ticket = Ticket.objects.get(pk=pk)
        ticket.status = 4
        ticket.save()
        return HttpResponseRedirect(reverse("tickets_app:reject_message", kwargs={"pk": pk}))

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(RejectTicketView, self).dispatch(
                request, *args, **kwargs
            )

class RejectMessageTicketView(LoginRequiredMixin, UpdateView):
    """vista para que el admin escriba el mensaje de motivo del rechazo"""

    model = Ticket
    template_name = "tickets/rejection_message.html"
    login_url = reverse_lazy("users_app:login")
    form_class = RejectionMessageForm

    def get_success_url(self, **kwargs):
        ticket = self.kwargs.get("pk")
        url = reverse("tickets_app:detail", kwargs={"pk": ticket})
        return url

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(RejectMessageTicketView, self).dispatch(
                request, *args, **kwargs
            )

class EditTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = "tickets/edit.html"
    success_url = reverse_lazy("tickets_app:all")
    login_url = reverse_lazy("users_app:login")

    def get_form_class(self):
        if self.request.user.role == 1:
            return AdminEditTicketForm
        if self.request.user.role == 2:
            return EditTicketForm


class CreateCommentView(LoginRequiredMixin, FormView):
    form_class = AddCommentForm
    template_name = "tickets/comment.html"
    login_url = reverse_lazy("users_app:login")

    def get_success_url(self, **kwargs):
        ticket = self.kwargs.get("ticket_id")
        if self.request.user.role == 3:
            url = reverse("tickets_app:detail", kwargs={"pk": ticket})
        else:
            url = reverse("tickets_app:edit", kwargs={"pk": ticket})
        return url

    def form_valid(self, form):
        Comment.objects.create(
            user=self.request.user,
            ticket=Ticket.objects.get(pk=self.kwargs["ticket_id"]),
            content=form.cleaned_data["content"],
            file=form.cleaned_data["file"],
        )
        return super().form_valid(form)


class ThanksView(LoginRequiredMixin, TemplateView):
    template_name = "tickets/thanks.html"
    login_url = reverse_lazy("users_app:login")


def export_tickets(request):
    agents = User.objects.filter(role=2)
    categories = Category.objects.all()
    today = datetime.today().strftime('%Y-%m-%d')
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
        #lines.append(ticket.created_at)
        lines.append(" ")

    for line in lines:
        content.textLine(line)

    my_canvas.drawText(content)
    my_canvas.showPage()
    my_canvas.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="tickets.pdf")


def export_tickets_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tickets.csv'

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
    writer.writerow([
        'Autor',
        'Email',
        'Título',
        'Estado',
        'Urgencia',
        'Categoría',
        'Agente',
        'Fecha de creación',
        'Ver ticket',
        'Motivo de rechazo',
    ])

    for ticket in tickets:
        writer.writerow([
            str(ticket.user.persona),
            ticket.email,
            ticket.title,
            ticket.get_status_display(),
            ticket.get_urgency_display(),
            ticket.category.title,
            ticket.agent.persona if ticket.agent else "No asignado",
            ticket.created_at.strftime("%d-%m-%Y %H:%M"),
            request.build_absolute_uri(reverse('tickets_app:detail',  kwargs={"pk": ticket.id})),
            ticket.rejection_message
        ])

    return response