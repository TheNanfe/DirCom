from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.users.urls")),
    path("", include("applications.core.urls")),
    path("pre_ticket/", include("applications.preTicket.urls")),
]
