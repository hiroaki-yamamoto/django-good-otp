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
        self.otp_secrets = OTPSecrets.objects.create(
            user=self.users[0], secret=("").join([
                random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
                for ignore in range(16)
            ])
        )
        self.req = RequestFactory().get("/test")

    @patch("django_otp.backends.ModelBackend.authenticate")
    def test_backend(self, auth):
        """Auth function should be called."""
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
