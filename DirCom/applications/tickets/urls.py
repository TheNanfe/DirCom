from django.urls import path
from . import views

app_name = "tickets_app"

urlpatterns = [
    path("", views.AllTicketsView.as_view(), name="all"),
    path("csv/", views.export_tickets_csv, name="csv"),
    path("exportar/", views.export_tickets, name="export"),
    path("nuevo/", views.CreateTicketView.as_view(), name="create"),
    path("thanks/", views.ThanksView.as_view(), name="thanks"),
    path("editar/<pk>/", views.EditTicketView.as_view(), name="edit"),
    path("revisar/<pk>/", views.AproveOrRejectTicketView.as_view(), name="check"),
    path("aprobar/<pk>/", views.AproveTicketView.as_view(), name="aprove"),
    path("rechazar/<pk>/", views.RejectTicketView.as_view(), name="reject"),
    path("mensaje/<pk>/", views.RejectMessageTicketView.as_view(), name="reject_message"),
    path("<pk>/", views.DetailTicketView.as_view(), name="detail"),
    path("<ticket_id>/comentar/", views.CreateCommentView.as_view(), name="comment"),
]