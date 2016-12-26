#!/usr/bin/env python
# coding=utf-8

"""Authentication function test."""


import random

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from django_otp.backends import OTPAuthenticationBackend, OTPAuthBackend
from django_otp.models import OTPSecrets


class BackendAliasTest(TestCase):
    """Backend alias test."""

    def test_alias(self):
        """Authentication backend alias should be OTPAuthenticationBackend."""
        self.assertIs(OTPAuthBackend, OTPAuthenticationBackend)


class AuthenticationBackendTest(TestCase):
    """Authentication function invokation test."""

    def setUp(self):
        """Setup."""
        self.backend = OTPAuthBackend()
        self.users = [
            get_user_model().objects.create_user(
                username=("test_{}").format(counter),
                password=("pw_{}").format(counter)
            ) for counter in range(2)
        ]
        self.otp_secret = OTPSecrets.objects.create(
            user=self.users[0], secret=self.__gen_otp_secret()
        )
        self.req = RequestFactory().get("/test")

    def __gen_otp_secret(self):
        """Generate OTP secret."""
        return ("").join([
            random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
            for ignore in range(16)
        ])

    @patch("django_otp.backends.ModelBackend.authenticate")
    def test_backend(self, auth):
        """Auth function should be called."""
        delattr(auth.return_value, "otp_secret")
        self.backend.authenticate(
            self.req, username="example", password="test",
            otp_auth=999999
        )
        auth.assert_called_once_with(
            request=self.req, username="example", password="test"
        )

    def test_user_auth(self):
        """The authentication should be succeeded without OTP."""
        user = self.backend.authenticate(
            self.req, username=self.users[1].username, password="pw_1"
        )
        self.assertEqual(user, self.users[1])

    def test_user_auth_failure_otp(self):
        """The authentication should be failed with OTP."""
        from pyotp.totp import TOTP
        provider = TOTP(self.otp_secret.secret)
        user = self.backend.authenticate(
            self.req, username=self.users[0].username, password="pw_0",
            otp_auth=str(
                (int(provider.now()) + 1) % 1000000
            ).zfill(provider.digits)
        )
        self.assertIsNone(user)

    def test_user_auth_success_otp(self):
        """The authentication should be succeeded with OTP."""
        from pyotp.totp import TOTP
        provider = TOTP(self.otp_secret.secret)
        user = self.backend.authenticate(
            self.req, username=self.users[0].username, password="pw_0",
            otp_auth=provider.now()
        )
        self.assertEqual(user, self.users[0])
