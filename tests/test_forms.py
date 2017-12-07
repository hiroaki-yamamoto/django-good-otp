#!/usr/bin/env python
# coding=utf-8

"""Form tests."""

from django import forms
from django.test import TestCase

from django_otp.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm

from .bases import DBIntegrationTestBase


class AuthFormTestBase(object):
    """Authentication form test base."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super(AuthFormTestBase, self).__init__(*args, **kwargs)
        self.form_cls = AuthenticationForm
        self.form = self.form_cls()


class AuthFormNormalInitTest(AuthFormTestBase, TestCase):
    """Normal authentication init test."""

    def form_type_test(self):
        """Inherit django's AuthenticationForm."""
        self.assertTrue(
            issubclass(self.form_cls, DjangoAuthForm),
            "The authentication form doesn't inherit Django's auth form."
        )

    def test_error_message(self):
        """invalid_login error message should be proper."""
        self.assertEqual(
            str(self.form.error_messages["invalid_login"]),
            "Please enter a correct %(username)s, password, and 2FA code. "
            "Note that either or both fields may be case-sensitive."
        )

    def test_form_field(self):
        """The form should have username, password, and OTP key."""
        check_map = {
            "username": forms.CharField,
            "password": forms.CharField,
            "otp_auth": forms.CharField
        }
        for (key, value) in check_map.items():
            self.assertIsInstance(self.form.fields[key], value)


class AuthenticationValidationSuccessTest(
    AuthFormTestBase, DBIntegrationTestBase, TestCase
):
    """2Fa form validation test."""

    def test_non_2fa(self):
        """The authentication should be succeeded for the user without 2fa."""
        form = self.form_cls(
            None, {"username": "test_1", "password": "pw_1"}
        )
        self.assertTrue(
            form.is_valid(), "Form is invalid: {}".format(dict(form.errors))
        )
        self.assertEqual(
            {"username": "test_1", "password": "pw_1", "otp_auth": ""},
            form.clean()
        )

    def test_2fa(self):
        """2fa should be valid."""
        from pyotp import TOTP
        otp = TOTP(self.secret.secret)
        query = {
            "username": "test_0",
            "password": "pw_0",
            "otp_auth": otp.now()
        }
        form = self.form_cls(None, query)
        self.assertTrue(
            form.is_valid(), "Form is invalid: {}".format(dict(form.errors))
        )
        self.assertDictEqual(query, form.clean())


class AuthenticationValidationFailureTest(
    AuthFormTestBase, DBIntegrationTestBase, TestCase
):
    """2Fa form invalidation test."""

    def test_username_empty(self):
        """The authentication should be failed due to empty username."""
        form = self.form_cls(
            None, {"password": "pw_2"}
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_password_empty(self):
        """The authentication should be failed due to empty password."""
        form = self.form_cls(
            None, {"username": "test_1"}
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_non_2fa(self):
        """The authentication should be failed because pw is not correct."""
        form = self.form_cls(
            None, {"username": "test_1", "password": "pw_2"}
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_2fa(self):
        """The authentication should be failed because otp is not correct."""
        from pyotp import TOTP
        otp = TOTP(self.secret.secret)
        query = {
            "username": "test_0",
            "password": "pw_0",
            "otp_auth": str((int(otp.now()) + 1) % 1000000).zfill(6)
        }
        form = self.form_cls(None, query)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
