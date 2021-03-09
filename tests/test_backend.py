#!/usr/bin/env python
# coding=utf-8

"""Authentication function test."""


from unittest import skipIf
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa

import django
from django.test import TestCase, RequestFactory

from django_otp.backends import OTPAuthenticationBackend, OTPAuthBackend

from .bases import DBIntegrationTestBase


class BackendAliasTest(TestCase):
    """Backend alias test."""

    def test_alias(self):
        """Authentication backend alias should be OTPAuthenticationBackend."""
        self.assertIs(OTPAuthBackend, OTPAuthenticationBackend)


@skipIf(
    tuple([int(s) for s in django.get_version().split(".")]) < (1, 11),
    "Django version must be later than 1.11"
)
class AuthenticationBackendTestDj111(DBIntegrationTestBase, TestCase):
    """Authentication function invokation test."""

    def setUp(self):
        """Set up."""
        super(AuthenticationBackendTestDj111, self).setUp()
        self.backend = OTPAuthBackend()
        self.req = RequestFactory().get("/test")

    @patch("django_otp.backends.ModelBackend.authenticate")
    def test_backend(self, auth):
        """Auth function should be called."""
        delattr(auth.return_value, "otp_secret")
        self.backend.authenticate(
            self.req, username="example", password="test",
            otp_auth=999999
        )
        auth.assert_called_once_with(
            self.req, username="example", password="test"
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
        provider = TOTP(self.secret.secret)
        user = self.backend.authenticate(
            self.req, username=self.users[0].username,
            password="pw_0", otp_auth=str(
                (int(provider.now()) + 1) % 1000000
            ).zfill(provider.digits)
        )
        self.assertIsNone(user)

    def test_user_auth_success_otp(self):
        """The authentication should be succeeded with OTP."""
        from pyotp.totp import TOTP
        provider = TOTP(self.secret.secret)
        user = self.backend.authenticate(
            self.req, username=self.users[0].username,
            password="pw_0", otp_auth=provider.now()
        )
        self.assertEqual(user, self.users[0])


@skipIf(
    tuple([int(s) for s in django.get_version().split(".")]) > (1, 10),
    "Django version must be earlier than 1.11"
)
class AuthenticationBackendTestDj110(DBIntegrationTestBase, TestCase):
    """Authentication function invokation test."""

    def setUp(self):
        """Set up."""
        super(AuthenticationBackendTestDj110, self).setUp()
        self.backend = OTPAuthBackend()

    @patch("django_otp.backends.ModelBackend.authenticate")
    def test_backend(self, auth):
        """Auth function should be called."""
        delattr(auth.return_value, "otp_secret")
        self.backend.authenticate(
            username="example", password="test", otp_auth=999999
        )
        auth.assert_called_once_with(
            username="example", password="test"
        )

    def test_user_auth(self):
        """The authentication should be succeeded without OTP."""
        user = self.backend.authenticate(
            username=self.users[1].username, password="pw_1"
        )
        self.assertEqual(user, self.users[1])

    def test_user_auth_failure_otp(self):
        """The authentication should be failed with OTP."""
        from pyotp.totp import TOTP
        provider = TOTP(self.secret.secret)
        user = self.backend.authenticate(
            username=self.users[0].username,
            password="pw_0", otp_auth=str(
                (int(provider.now()) + 1) % 1000000
            ).zfill(provider.digits)
        )
        self.assertIsNone(user)

    def test_user_auth_success_otp(self):
        """The authentication should be succeeded with OTP."""
        from pyotp.totp import TOTP
        provider = TOTP(self.secret.secret)
        user = self.backend.authenticate(
            username=self.users[0].username,
            password="pw_0", otp_auth=provider.now()
        )
        self.assertEqual(user, self.users[0])
