from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Q

from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from applications.tickets.models import Ticket

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    template_name = "core/home.html"
    login_url = reverse_lazy("users_app:login")
    context_object_name = "tickets"

    def get_queryset(self):
        # todos los tickets para el admin
        if self.request.user.role == 1:
            tickets = Ticket.objects.all().filter(
                ~Q(status=4)
            )[:10] # solo 10 resultados

        # solo tickets asignados al analista
        if self.request.user.role == 2:
            tickets = Ticket.objects.filter(agent=self.request.user).filter(
                ~Q(status=4)
            )[:5] # solo 5 resultados

        # solo tickets propios para el usuario
        if self.request.user.role == 3:
            tickets = Ticket.objects.filter(user=self.request.user)[:3] # solo 3 resultados
        return tickets


def send_notification(request):
    subject = "Notificación del DirCom"
    context = {
        "title": "Notificación del DirCom",
        "content": "Lorem ipsum dolor sit amet",
        "url": "localhost:8000/tickets/",
        "action_text": "Ver tickets",
    }
    html_content = render_to_string("core/email.html", context)
    text_content = striptags(html_content)
    print(request.user.persona.email)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_FROM, [request.user.persona.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()