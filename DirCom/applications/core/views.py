from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    login_url = reverse_lazy("users_app:login")
