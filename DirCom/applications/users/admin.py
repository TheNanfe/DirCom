from atexit import register
from django.contrib import admin
from .models import User, Persona

# Register your models here.
admin.site.register(User)
admin.site.register(Persona)