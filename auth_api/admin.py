from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


# Register your models here.
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = (
        "email",
        "user_name",
        "full_name",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering = ("-start_date",)
    list_display = (
        "id",
        "email",
        "profile_picture",
        "full_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "full_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        # ('Personal', {'fields': ('about',)}),
    )
    # formfield_overrides = {
    #     models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    # }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)
