from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
# django.contrib.auth es el módulo que nos permite implementar
# las funcionalidades de manejos de sesión en nuestras vistas
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .forms import UserRegisterForm, UserLoginForm
from .models import User


class UserRegisterView(FormView):
    """ vista para registrar nuevos usuarios """
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        # llamamos al método create_user que sobreescribimos
        # en el archivo managers.py
        User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["gov_id"],
            form.cleaned_data["custom_password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            city=form.cleaned_data["city"],
            phone=form.cleaned_data["phone"],
            vinc_type=form.cleaned_data["vinc_type"],
        )

        return super(UserRegisterView, self).form_valid(form)


class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("core_app:home")

    def form_valid(self, form):
        # authenticate revisa que las credenciales proporcionadas por
        # el usuario coincidan con nuestra base de datos, si el usuario
        # es correcto entonces devuelve un usuario, sino, devuelve NONE
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        # una vez autenticamos un usuario inicia una sesión en nuestro
        # sistema mediante el médoto login, la sesión se guarda en el
        # request de cada petición
        login(self.request, user)

        return super(UserLoginView, self).form_valid(form)


class UserLogoutView(View):
    """ vista para cerrar la sesión de los usuarios """
    def get(self, request, *args, **kwargs):
        # el método logout hace lo contrario al método login
        # en vez de guardar la sesión en la request, la borra
        # entonces el usuario ya no está autenticado
        logout(request)
        return HttpResponseRedirect(reverse("users_app:login"))
