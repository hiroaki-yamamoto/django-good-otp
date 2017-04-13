#!/usr/bin/env python
# coding=utf-8

"""Authentication funciton tests."""

import django
from unittest import skipIf

try:
    from unittest.mock import ANY, patch
except ImportError:
    from mock import ANY, patch  # noqa

from django.contrib.auth import authenticate
from django.test import TestCase, RequestFactory

from django_otp.backends import OTPAuthenticationBackend


@skipIf(
    tuple([int(s) for s in django.get_version().split(".")]) < (1, 11),
    "Django version must be later than 1.11"
)
class AuthenticateFunctionTestDj111(TestCase):
    """Authenticate function test."""

    def setUp(self):
        """Setup."""
        self.request = RequestFactory().get("/")

    @patch.object(OTPAuthenticationBackend, "authenticate", autospec=True)
    def test_authenticate(self, backend_authenticate):
        """Authenticate should call proper authentication function."""
        backend_authenticate.__name__ = "authenticate"
        query = {"username": "test_1", "password": "pw_1"}
        authenticate(self.request, **query)
        backend_authenticate.assert_called_once_with(
            ANY, self.request, **query
        )

        # ...It means you can authenticate the user with 2fa by using
        # django's authenticate function.


@skipIf(
    tuple([int(s) for s in django.get_version().split(".")]) > (1, 10),
    "Django version must be earlier than 1.11"
)
class AuthenticateFunctionTestDj110(TestCase):
    """Authenticate function test."""

    @patch.object(OTPAuthenticationBackend, "authenticate", autospec=True)
    def test_authenticate(self, backend_authenticate):
        """Authenticate should call proper authentication function."""
        backend_authenticate.__name__ = "authenticate"
        query = {"username": "test_1", "password": "pw_1"}
        authenticate(**query)
        backend_authenticate.assert_called_once_with(
            ANY, **query
        )

        # ...It means you can authenticate the user with 2fa by using
        # django's authenticate function.
