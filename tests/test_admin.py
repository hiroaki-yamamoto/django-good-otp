#!/usr/bin/env python
# coding=utf-8

"""Administration panel test."""

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # nonqa

from django.contrib import admin
from django.test import TestCase

from django_otp.models import OTPSecrets
from django_otp.admin import OTPAdmin, AdminSite


class AdminPanelRegistrationTest(TestCase):
    """settings.ENABLE_OTP_ADMIN = True test."""

    def setUp(self):
        """Setup."""
        self.admin = OTPAdmin

    def test_panel_type(self):
        """The admin panel should be displayed."""
        self.assertTrue(issubclass(self.admin, admin.ModelAdmin))

    @patch("django_otp.admin.admin.site.register")
    def test_enabled_panel(self, register):
        """The registration function should be called with the Secret Model."""
        self.admin.enable()
        register.assert_called_once_with(OTPSecrets, self.admin)


class AdminSiteInitialStateTest(TestCase):
    """Admin site initial state test."""

    def setUp(self):
        """Setup."""
        self.data = {"test1": "test", "test2": "test0"}

    def test_register_dict(self):
        """The registry should be cloned."""
        otp_admin = None
        with patch.dict(admin.site._registry, self.data, clear=True):
            otp_admin = AdminSite()
        self.assertDictEqual(self.data, otp_admin._registry)


class AdminSiteInitialStateInheritTrueTest(TestCase):
    """Admin site initial state test when inherit_panels=Truthy."""

    def setUp(self):
        """Setup."""
        self.data = {"test1": "test", "test2": "test0"}

    def test_register_dict(self):
        """The registry should be cloned."""
        otp_admin = None
        with patch.dict(admin.site._registry, self.data, clear=True):
            otp_admin = AdminSite(inherit_panels=True)
        self.assertDictEqual(self.data, otp_admin._registry)


class AdminSiteInitialStateInheritFalseTest(TestCase):
    """Admin site initial state test when inherit_panels=Falsy."""

    def test_register_dict(self):
        """The registry shouldn't be cloned."""
        otp_admin = AdminSite(inherit_panels=False)
        self.assertDictEqual({}, otp_admin._registry)
