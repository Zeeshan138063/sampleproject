"""Register your models here."""
from django.contrib import admin
from .models import User, EmailStatus

admin.site.register(User)
admin.site.register(EmailStatus)
