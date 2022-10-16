from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ticket


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