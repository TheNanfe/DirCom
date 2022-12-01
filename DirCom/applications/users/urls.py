from django.urls import path
from . import views

app_name = "users_app"

urlpatterns = [
    path("nuevo/", views.PersonaRegisterView.as_view(), name="add_persona"),
    path("editar/", views.PersonaUpdateProfileView.as_view(), name="update_persona"),
    path("borrar-perfil/", views.PersonaDeleteProfileView.as_view(), name="delete_persona"),
    path("registro/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("password/", views.UpdatePasswordView.as_view(), name="password"),
    path("perfil/", views.MyProfileView.as_view(), name="profile"),
    path("usuarios/", views.AllUsersView.as_view(), name="all"),
    path("usuarios/<username>/", views.UserDetailView.as_view(), name="detail"),
    path("editar/<pk>/", views.UserUpdateView.as_view(), name="edit"),
    path("update/<pk>/", views.UserUpdateRoleView.as_view(), name="update"),
    path("eliminar/<username>/", views.SwitchStatusUserView.as_view(), name="switch"),
    path("recuperar/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("recuperar/<username>/", views.NewPasswordView.as_view(), name="new_password"),
    path("enviado/", views.ResetPasswordSuccessView.as_view(), name="reset_password_success"),
]