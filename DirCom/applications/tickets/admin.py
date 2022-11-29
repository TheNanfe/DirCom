from atexit import register
from django.contrib import admin
from .models import Comment, Ticket

# Register your models here.
admin.site.register(Comment)
admin.site.register(Ticket)