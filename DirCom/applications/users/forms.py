from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Persona

class AddPersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(AddPersonaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UpdatePersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(UpdatePersonaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(UserCreationForm):
    """
    clase para el formulario de creación de usuarios del admin
    """

    class Meta:
        model = User
        fields = ("persona",)


class CustomUserChangeForm(UserChangeForm):
    """
    clase para el formulario de edición de usuarios del admin
    """

    class Meta:
        model = User
        fields = ("persona",)


class UserRegisterForm(forms.ModelForm):
    """
    creamos los campos para el formulario de registro de nuestra app,
    como la contraseña no se guarda como texto plano, sino mediante
    un método especial llamado set_password que se ejecuta en el método
    privado _create_user que sobreescribimos en el archivo managers.py,
    entonces debido a esto creamos el campo de contraseña por separado
    """

    custom_password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Introduzca su contraseña"}),
    )

    # campo para validar que el usuario metió la misma contraseña 2 veces
    repeat_password = forms.CharField(
        label="Repetir contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repita su contraseña"}),
    )

    class Meta:
        model = User  # el modelo sobre el cual trabajamos

        # la lista de campos que necesita nuestro modelo
        fields = (
            "username",
            "persona",
            "role"
        )

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['persona'].queryset = Persona.objects.filter(user=None)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_repeat_password(self):
        """método para validar que el usuario escribió bien su contraseña"""
        if self.cleaned_data["custom_password"] != self.cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Las contraseñas no coinciden")

        """ método para validar que el usuario tiene una contraseña mayor a 5 carácteres """
        if len(self.cleaned_data["custom_password"]) <= 5:
            self.add_error("custom_password", "La contraseña es muy corta")


class UserUpdateRoleForm(forms.ModelForm):
    class Meta:
        model = User  # el modelo sobre el cual trabajamos

        # la lista de campos que necesita nuestro modelo
        fields = (
            "username",
            "persona",
            "role"
        )

    def __init__(self, *args, **kwargs):
        super(UserUpdateRoleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
    """
    clase que controla el inicio de sesión de los usuarios , como no está vinculado
    a ningún modelo ya que no realizaremos ninguna acción sobre la base de datos,
    entonces tenemos que crear ambos campos a medida y necesidad
    """

    username = forms.CharField(
        label="Nombre de usuario o correo electrónico",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Introduzca su usuario"}),
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Introduzca su contraseña"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """método para validar las credenciales del usuario"""
        cleaned_data = super(UserLoginForm, self).clean()
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if not authenticate(
            username=username,
            password=password,
        ):
            # si el usuario proporciona credenciales incorrectas entonces
            # podrá ver este aviso en el formulario de login
            raise forms.ValidationError("Datos incorrectos")

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    # campo para validar su contraseña actual
    current_password = forms.CharField(
        label="Contraseña actual",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Introduzca su contraseña actual"}
        ),
    )

    # campo para nueva contraseña
    custom_password = forms.CharField(
        label="Contraseña nueva",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Introduzca su nueva contraseña"}
        ),
    )

    # campo para validar que el usuario metió la misma contraseña 2 veces
    repeat_password = forms.CharField(
        label="Repetir contraseña nueva",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repita su nueva contraseña"}),
    )

    def __init__(self, user, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.user = user
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def clean(self):
        """método para validar las credenciales del usuario"""
        cleaned_data = super(UpdatePasswordForm, self).clean()
        username = self.user.username
        password = self.cleaned_data["current_password"]

        if not authenticate(
            username=username,
            password=password,
        ):
            # si el usuario proporciona credenciales incorrectas entonces
            # podrá ver este aviso en el formulario de login
            raise forms.ValidationError("Contraseña actual incorrecta")

        return self.cleaned_data

    def clean_repeat_password(self):
        """método para validar que el usuario escribió bien su contraseña"""
        if self.cleaned_data["custom_password"] != self.cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Las contraseñas no coinciden")

        """ método para validar que el usuario tiene una contraseña mayor a 5 carácteres """
        if len(self.cleaned_data["custom_password"]) <= 5:
            self.add_error("custom_password", "La contraseña es muy corta")


class ResetPasswordForm(forms.Form):
    # campo para introducir tu correo
    email = forms.EmailField(
        label="Introduce tu email",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class NewPasswordForm(forms.Form):

    # campo para nueva contraseña
    custom_password = forms.CharField(
        label="Contraseña nueva",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Introduzca su nueva contraseña"}
        ),
    )

    # campo para validar que el usuario metió la misma contraseña 2 veces
    repeat_password = forms.CharField(
        label="Repetir contraseña nueva",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repita su nueva contraseña"}),
    )

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def clean_repeat_password(self):
        """método para validar que el usuario escribió bien su contraseña"""
        if self.cleaned_data["custom_password"] != self.cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Las contraseñas no coinciden")

        """ método para validar que el usuario tiene una contraseña mayor a 5 carácteres """
        if len(self.cleaned_data["custom_password"]) <= 5:
            self.add_error("custom_password", "La contraseña es muy corta")