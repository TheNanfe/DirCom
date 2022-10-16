from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ticket
from .forms import AddTicketForm


class AllTicketsView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/all.html"
    context_object_name = "tickets"
    login_url = reverse_lazy("users_app:login")

class DetailTicketView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "tickets/detail.html"
    context_object_name = "ticket"
    login_url = reverse_lazy("users_app:login")

class CreateTicketView(LoginRequiredMixin, FormView):
    form_class = AddTicketForm
    success_url = "/"
    template_name = "tickets/create.html"
    login_url = reverse_lazy("users_app:login")