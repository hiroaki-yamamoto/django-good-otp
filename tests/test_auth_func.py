#!/usr/bin/env python
# coding=utf-8

"""Authentication funciton tests."""

try:
    from unittest.mock import ANY, patch
except ImportError:
    from mock import ANY, patch  # noqa

from django.contrib.auth import authenticate
from django.test import TestCase

from django_otp.backends import OTPAuthenticationBackend


class AuthenticateFunctionTest(TestCase):
    """Authenticate function test."""

    @patch.object(OTPAuthenticationBackend, "authenticate", autospec=True)
    def test_authenticate(self, auth_mock):
        """Authenticate should call proper authentication function."""
        auth_mock.__name__ = "authenticate"
        query = {"username": "test_1", "password": "pw_1"}
        authenticate(**query)
        auth_mock.assert_called_once_with(ANY, **query)

        # ...It means you can authenticate the user with 2fa by using
        # django's authenticate function.
