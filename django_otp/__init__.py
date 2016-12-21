#!/usr/bin/env python
# coding=utf-8

"""Django OTP Implementation."""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoOTP(AppConfig):
    """Django OTP configuration."""

    name = "django_otp"
    label = "django_otp"
    verbose_name = _("Django OTP")
