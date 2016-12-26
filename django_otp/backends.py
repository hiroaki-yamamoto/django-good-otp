#!/usr/bin/env python
# coding=utf-8

"""
OTP Authentication Backends.

Any authentication that requires OTP authentication should use below backends
or inherit them.
"""

from django.contrib.auth.backends import ModelBackend
from pyotp import TOTP


class OTPAuthenticationBackend(ModelBackend):
    """OTPAuthenticationBackend."""

    def authenticate(self, **kwargs):
        """Authentication form."""
        otp_auth = kwargs.pop("otp_auth", None)

        user = super(OTPAuthenticationBackend, self).authenticate(**kwargs)
        if hasattr(user, "otp_secret"):
            auth_provider = TOTP(user.otp_secret.secret)
            if not auth_provider.verify(otp_auth):
                user = None
        return user


OTPAuthBackend = OTPAuthenticationBackend
