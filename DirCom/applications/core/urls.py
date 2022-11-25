from django.urls import path
from . import views

app_name = "core_app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("notificar/", views.send_notification, name="notification"),
]