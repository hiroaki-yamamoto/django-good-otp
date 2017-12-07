#!/usr/bin/env python
# coding=utf-8

"""
OTP Authentication Backends.

Any authentication that requires OTP authentication should use below backends
or inherit them.
"""

from functools import partial

import django
from django.contrib.auth.backends import ModelBackend
from pyotp import TOTP


class OTPAuthenticationBackend(ModelBackend):
    """OTPAuthenticationBackend."""

    def authenticate(self, request=None, **kwargs):
        """Check form validity."""
        django_version = tuple(
            [int(s) for s in django.get_version().split(".")]
        )
        otp_auth = kwargs.pop("otp_auth", None)
        auth_user = partial(
            super(OTPAuthenticationBackend, self).authenticate,
            **kwargs
        )

        user = auth_user() if django_version < (1, 11) else auth_user(request)
        if hasattr(user, "otp_secret"):
            auth_provider = TOTP(user.otp_secret.secret)
            if not auth_provider.verify(otp_auth):
                user = None
        return user


OTPAuthBackend = OTPAuthenticationBackend
