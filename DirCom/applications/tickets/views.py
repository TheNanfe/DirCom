from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Comment, Ticket
from .forms import AddTicketForm, AddCommentForm, AdminEditTicketForm, EditTicketForm


class AllTicketsView(LoginRequiredMixin, ListView):
    template_name = "tickets/all.html"
    context_object_name = "tickets"
    login_url = reverse_lazy("users_app:login")

    def get_queryset(self):
        title = self.request.GET.get("title", "")
        # todos los tickets para el admin
        if self.request.user.role == 1:
            tickets = Ticket.objects.all()
        # solo tickets asignados al analista
        if self.request.user.role == 2:
            tickets = Ticket.objects.filter(agent=self.request.user).filter(
                ~Q(status=4)
            )
        # solo tickets propios para el usuario
        if self.request.user.role == 3:
            tickets = Ticket.objects.filter(user=self.request.user)
        filtered = tickets.filter(title__contains=title)
        return filtered

    def get_context_data(self, **kwargs):
        context = super(AllTicketsView, self).get_context_data(**kwargs)
        context["title"] = self.request.GET.get("title", "")
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
