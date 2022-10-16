from django.urls import path
from . import views

app_name = "tickets_app"

urlpatterns = [
    path("", views.AllTicketsView.as_view(), name="all"),
    path("<pk>/", views.DetailTicketView.as_view(), name="detail"),
    # path("nuevo/", views.PersonaRegisterView.as_view(), name="add_persona"),
    # path("editar/", views.PersonaUpdateProfileView.as_view(), name="update_persona"),
    # path("borrar-ticket/", views.PersonaDeleteProfileView.as_view(), name="delete_persona"),
]