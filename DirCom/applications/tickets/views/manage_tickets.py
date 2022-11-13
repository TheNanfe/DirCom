import json

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect

from ..ticket_utils import *
from applications.tickets.models import Comment, Ticket, Category
from applications.tickets.forms import (
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sub_category = Ticket.objects.filter(pk=self.kwargs['pk']).values("sub_category")
        try:
            sub_category_dict = sub_category[0]
            sub_category_dict = parse_json_data(sub_category_dict["sub_category"])
            service_key = None
            for key in sub_category_dict:
                service_key = key

            service_extra_info = sub_category_dict[service_key]
            context["service_type"] = get_service_name(service_key)
            context["service_extra_info"] = service_extra_info
        except Exception as e:
            print("Exception has occured --> ", e)
            context["service_type"] = "---"
        return context


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
        service_info = get_json_data(form)
        ticket = Ticket.objects.create(
            user=self.request.user,
            email=form.cleaned_data["email"],
            title=form.cleaned_data["title"],
            content=form.cleaned_data["content"],
            file=form.cleaned_data["file"],
            category=form.cleaned_data["category"],
            sub_category=json.dumps(service_info),
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sub_category = Ticket.objects.filter(pk=self.kwargs['pk']).values("sub_category")
        try:
            sub_category_dict = sub_category[0]
            sub_category_dict = parse_json_data(sub_category_dict["sub_category"])
            service_key = None
            for key in sub_category_dict:
                service_key = key

            service_extra_info = sub_category_dict[service_key]
            context["service_type"] = get_service_name(service_key)
            context["service_extra_info"] = service_extra_info
        except Exception as e:
            print("Exception has occured --> ", e)
            context["service_type"] = "---"
        return context


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