from django import forms
from django.contrib.auth import authenticate

from .models import User


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
        model = User # el modelo sobre el cual trabajamos

        # la lista de campos que necesita nuestro modelo
        fields = (
            "username", 
            "gov_id", 
            "email", 
            "first_name", 
            "last_name",
            "city",
            "phone",
            "area",
            "vinc_type",
        )

    def clean_repeat_password(self):
        """ método para validar que el usuario escribió bien su contraseña """
        if self.cleaned_data["custom_password"] != self.cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Las contraseñas no coinciden")

        """ método para validar que el usuario tiene una contraseña mayor a 5 carácteres """
        if len(self.cleaned_data["custom_password"]) <= 5:
            self.add_error("custom_password", "La contraseña es muy corta")


class UserLoginForm(forms.Form):
    """ 
        clase que controla el inicio de sesión de los usuarios , como no está vinculado
        a ningún modelo ya que no realizaremos ninguna acción sobre la base de datos,
        entonces tenemos que crear ambos campos a medida y necesidad
    """

    username = forms.CharField(
        label="Nombre de usuario",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Introduzca su usuario"}),
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Introduzca su contraseña"}),
    )

    def clean(self):
        """ método para validar las credenciales del usuario """
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
