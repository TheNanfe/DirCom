import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods
from .models import Notification
from django.http.response import JsonResponse, HttpResponse

from .notifications_utils import get_notifications_for_user


# Create your views here.
@require_http_methods(["POST", "GET"])
def get_notifications(request):
    if not request.user.is_authenticated:
        return reverse_lazy("users_app:login")

    if request.method == "POST":
        user_id = int(request.user.pk)
        user_notifications = Notification.objects.filter(user_id=user_id).order_by("-id")
        user_notifications.update(status="VIEWED")
        user_notifications = user_notifications[:10]
        notifications = get_notifications_for_user(user_notifications)
        return HttpResponse(render(request, "notifications/notification_popup.html", notifications))


@require_http_methods(["POST"])
def update_read_status(request):
    if not request.user.is_authenticated:
        return reverse_lazy("users_app:login")

    if request.method == "POST":
        not_id = request.POST["notification_id"]
        Notification.objects.filter(id=not_id).update(status_read="READ")
        message = ("Notification #%s successfully updated!", not_id)
        return JsonResponse({"message": message})


@require_http_methods(["GET"])
def show_all_notifications(request, pk):
    if not request.user.is_authenticated:
        return reverse_lazy("users_app:login")

    if request.method == 'GET':
        user_notifications = Notification.objects.filter(user_id=pk).order_by("-id")
        notifications = get_notifications_for_user(user_notifications)
        return HttpResponse(render(request, "notifications/list_all_notifications.html", notifications))
