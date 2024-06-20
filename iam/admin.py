# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import AppUser

admin.site.register(AppUser)
admin.site.register(Permission)
