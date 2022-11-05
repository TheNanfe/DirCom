from django.shortcuts import redirect, render
from django.views.generic import (
    View,
    CreateView,
    UpdateView,
    TemplateView,
    ListView,
    DetailView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse

# django.contrib.auth es el módulo que nos permite implementar
# las funcionalidades de manejos de sesión en nuestras vistas
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .forms import (
    AddPersonaForm,
    UpdatePersonaForm,
    UserRegisterForm,
    UserLoginForm,
    UpdatePasswordForm,
)
from .models import User, Persona


class PersonaRegisterView(LoginRequiredMixin, CreateView):
    """vista para que el admin pueda crear personas"""

    form_class = AddPersonaForm
    template_name = "users/add_persona.html"
    success_url = reverse_lazy("users_app:register")
    login_url = reverse_lazy("users_app:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(PersonaRegisterView, self).dispatch(request, *args, **kwargs)


class PersonaUpdateProfileView(LoginRequiredMixin, UpdateView):
    """vista para que los usuarios puedan editar sus datos"""

    form_class = UpdatePersonaForm
    template_name = "users/edit_persona.html"
    success_url = reverse_lazy("users_app:profile")
    login_url = reverse_lazy("users_app:login")

    def get_object(self):
        return Persona.objects.get(pk=self.request.user.persona_id)


class PersonaDeleteProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users_app:login")

    """ vista para eliminar la cuenta de un usuario """

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("users_app:login"))


class UserRegisterView(FormView):
    """vista para registrar nuevos usuarios"""

    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(UserRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # llamamos al método create_user que sobreescribimos
        # en el archivo managers.py
        User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["persona"],
            form.cleaned_data["custom_password"],
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


class UserLogoutView(LoginRequiredMixin, View):
    """vista para cerrar la sesión de los usuarios"""

    login_url = reverse_lazy("users_app:login")

    def get(self, request, *args, **kwargs):
        # el método logout hace lo contrario al método login
        # en vez de guardar la sesión en la request, la borra
        # entonces el usuario ya no está autenticado
        logout(request)
        return HttpResponseRedirect(reverse("users_app:login"))


class UpdatePasswordView(LoginRequiredMixin, FormView):
    """vista para que los usuarios cambien su contraseña"""

    template_name = "users/password.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("users_app:login")
    login_url = reverse_lazy("users_app:login")

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        is_authenticated = authenticate(
            username=user.username, password=form.cleaned_data["current_password"]
        )

        if is_authenticated:
            new_password = form.cleaned_data["custom_password"]
            user.set_password(new_password)
            user.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class MyProfileView(LoginRequiredMixin, TemplateView):
    """vista para que los usuarios vean su perfil"""

    template_name = "users/profile.html"
    login_url = reverse_lazy("users_app:login")


class AllUsersView(LoginRequiredMixin, ListView):
    """vista para que el admin pueda ver la lista de usuarios del sistema"""

    model = User
    template_name = "users/all.html"
    context_object_name = "users"
    login_url = reverse_lazy("users_app:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(AllUsersView, self).dispatch(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    """vista para que el admin pueda visitar la cuenta de un usuario"""

    model = User
    template_name = "users/detail.html"
    context_object_name = "usuario"
    slug_url_kwarg = "username"
    slug_field = "username"
    login_url = reverse_lazy("users_app:login")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """vista para que el admin edite a los usuarios"""

    model = Persona
    form_class = UpdatePersonaForm
    template_name = "users/edit.html"
    success_url = reverse_lazy("users_app:all")
    login_url = reverse_lazy("users_app:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class SwitchStatusUserView(LoginRequiredMixin, View):
    """vista para que el admin pueda dar de alta o baja la cuenta de un usuario"""

    login_url = reverse_lazy("users_app:login")

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username", "default")
        user = User.objects.get(username=username)
        user.is_active = not user.is_active
        user.save()
        return HttpResponseRedirect(reverse("users_app:all"))

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 1:
            return redirect("core_app:home")
        else:
            return super(SwitchStatusUserView, self).dispatch(request, *args, **kwargs)
