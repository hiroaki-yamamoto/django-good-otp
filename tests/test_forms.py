#!/usr/bin/env python
# coding=utf-8

"""Form tests."""

from unittest import skip

from django import forms
from django.test import TestCase

from django_otp.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm


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
        """The form should inherit django's AuthenticationForm."""
        self.assertTrue(
            issubclass(self.form_cls, DjangoAuthForm),
            "The authentication form doesn't inherit Django's auth form."
        )

    def test_form_field(self):
        """The form should have username, password, and OTP key."""
        check_map = {
            "username": forms.CharField,
            "password": forms.CharField,
            "otp_auth": forms.IntegerField
        }
        for (key, value) in check_map.items():
            self.assertIsInstance(self.form.fields[key], value)


@skip("Not Implemented Yet")
class AuthenticationValidationTest(AuthFormTestBase, TestCase):
    """2Fa form validation test."""

    def setUp(self):
        """Setup."""
        raise NotImplementedError()

    def test_2fa(self):
        """2fa should be valid."""
        raise NotImplementedError()
