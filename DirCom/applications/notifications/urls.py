from django.urls import path
from . import views

app_name = "notifications_app"

urlpatterns = [
    path("get_notifications/", views.get_notifications, name="get_notifications"),
    path("update_read_status/", views.update_read_status, name="update_read_status"),
    path("show_all_notifications/<pk>", views.show_all_notifications, name="show_all_notifications"),
    ]
