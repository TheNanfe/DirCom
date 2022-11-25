from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Q
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