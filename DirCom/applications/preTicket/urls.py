from django.urls import path
from . import views

app_name = "pre_ticket_app"

urlpatterns = [
    path("creation_form", views.pre_ticket_creation_form, name="pre_ticket_creation_form"),
    path("change_status", views.pre_ticket_status_change, name="pre_ticket_status_change"),
    path("change_status/<str:pk>", views.pre_ticket_status_change, name="pre_ticket_status_change"),
    path("list_pre_tickets", views.list_pre_tickets, name="list_pre_tickets")
]