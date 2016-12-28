#!/usr/bin/env python
# coding=utf-8

"""OTP Admin Panel."""

from django.contrib import admin
from .models import OTPSecrets


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
