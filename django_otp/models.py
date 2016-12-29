#!/usr/bin/env python
# coding=utf-8

"""Database models."""

from django.db import models
from django.conf import settings


class OTPSecrets(models.Model):
    """OTP Secret key model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="otp_secret",
        primary_key=True
    )
    secret = models.CharField(max_length=16, db_index=True)
    issuer_name = models.CharField(
        max_length=40, db_index=True, null=False, blank=True
    )
