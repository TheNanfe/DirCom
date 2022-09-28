from django.urls import path
from . import views

app_name = "preTicket_app"

urlpatterns = [
    path("creation_form", views.pre_ticket_creation_form, name="pre_ticket_creation_form"),
]