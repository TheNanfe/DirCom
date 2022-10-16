from atexit import register
from django.contrib import admin
from .models import Category, Comment, Ticket

# Register your models here.
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Ticket)