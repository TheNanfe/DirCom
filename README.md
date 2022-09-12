# DirCom

Repositorio Proyecto 2. FPUNA, 2022. HL, SDV, RV


## Pasos para la instalación


1. Crear un entorno virtual para tu proyecto y activarlo

2. Correr el comando `pip install -r requirements.txt` para instalar todas las dependencias del proyecto

3. Crear la base de datos para el proyecto, preferiblemente llamada 'dircom'

4. Correr el comando `python manage.py makemigrations` y luego `python manage.py migrate`

5. Para crear tu usuario es necesario primero: crear una instancia de Persona y luego podrás crear tu superadmin, así que primero corre el comando `python manage.py dircom <tu_documento_de_identidad> <tu_email>`. Ej: `python manage.py dircom 3214532 juan@gmail.com`. De esta manera creas el primer usuario del sistema, así que tiene el id=1

6. Ahora, para crear un superuser debes correr el comando `python manage.py createsuperuser`, y te pedirá un nombre de usuario, un id de persona, que es el que acabas de crear (1) y una contraseña.

7. Listo!