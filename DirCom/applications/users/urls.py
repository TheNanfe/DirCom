from django.urls import path
from . import views

app_name = "users_app"

urlpatterns = [
    path("nuevo/", views.PersonaRegisterView.as_view(), name="add_persona"),
    path("editar/", views.PersonaUpdateProfileView.as_view(), name="update_persona"),
    path("registro/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("password/", views.UpdatePasswordView.as_view(), name="password"),
]