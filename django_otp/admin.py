#!/usr/bin/env python
# coding=utf-8

"""OTP Admin Panel."""

from django.contrib import admin
from os import path
from .models import OTPSecrets
from .forms import AuthenticationForm


class OTPAdmin(admin.ModelAdmin):
    """OTPSecret Admin."""

    list_display = ("user", )
    search_fields = (
        "user__email", "user__first_name", "user__last_name",
        "user__username"
    )

    @classmethod
    def enable(cls):
        """Assign the model to the panel."""
        admin.site.register(OTPSecrets, cls)


class AdminSite(admin.AdminSite):
    """AdminSite."""

    login_form = AuthenticationForm
    login_template = path.join(
        path.abspath(path.dirname(__file__)),
        "templates", "1_10", "login.html"
    )
