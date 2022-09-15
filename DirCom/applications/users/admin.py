from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Persona
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'persona', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'role', 'persona', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('persona', 'password1', 'password2', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ('persona',)
    ordering = ('username',)

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Persona)