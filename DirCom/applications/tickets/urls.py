from django.urls import path
from . import views

app_name = "tickets_app"

urlpatterns = [
    path("", views.AllTicketsView.as_view(), name="all"),
    path("nuevo/", views.CreateTicketView.as_view(), name="create"),
    path("thanks/", views.ThanksView.as_view(), name="thanks"),
    path("editar/<pk>/", views.EditTicketView.as_view(), name="edit"),
    path("revisar/<pk>/", views.AproveOrRejectTicketView.as_view(), name="check"),
    path("<pk>/", views.DetailTicketView.as_view(), name="detail"),
    path("<ticket_id>/comentar/", views.CreateCommentView.as_view(), name="comment"),
]