from django.urls import path
from . import views

app_name = "reports_app"

urlpatterns = [
    path("", views.ReportsIndex.as_view(), name="reports_index"),
    path("tickets_reports", views.tickets_reports, name="tickets_reports"),

]