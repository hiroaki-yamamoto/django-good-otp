#!/usr/bin/env python
# coding=utf-8

"""Administration panel test."""

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # nonqa

from django.contrib.admin import ModelAdmin
from django.test import TestCase

from django_otp.models import OTPSecrets
from django_otp.admin import OTPAdmin


class AdminPanelRegistrationTest(TestCase):
    """settings.ENABLE_OTP_ADMIN = True test."""

    def setUp(self):
        """Setup."""
        self.admin = OTPAdmin

    def test_panel_type(self):
        """The admin panel should be displayed."""
        self.assertTrue(issubclass(self.admin, ModelAdmin))

    @patch("django_otp.admin.admin.site.register")
    def test_enabled_panel(self, register):
        """The registration function should be called with the Secret Model."""
        self.admin.enable()
        register.assert_called_once_with(OTPSecrets, self.admin)
