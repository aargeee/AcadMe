# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import AppUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "last_login")}),
        (
            ("Permissions"),
            {"fields": ("is_staff", "is_active", "is_superuser", "groups")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "password1", "password2"),
            },
        ),
    )


admin.site.register(AppUser, CustomUserAdmin)
admin.site.register(Permission)
