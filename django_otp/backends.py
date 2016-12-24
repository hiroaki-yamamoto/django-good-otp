#!/usr/bin/env python
# coding=utf-8

"""
OTP Authentication Backends.

Any authentication that requires OTP authentication should use below backends
or inherit them.
"""

from django.contrib.auth.backends import ModelBackend


class OTPAuthenticationBackend(ModelBackend):
    """OTPAuthenticationBackend."""

    def authenticate(
        self, request, username=None, password=None, otp_auth=None, **kwargs
    ):
        """Authentication form."""
        user = super(OTPAuthenticationBackend, self).authenticate(
            request=request, username=username, password=password, **kwargs
        )
        return user


OTPAuthBackend = OTPAuthenticationBackend
