from django.shortcuts import redirect, render
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

    def dispatch(self, request, *args, **kwargs):
        if(request.user.role != 4):
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
