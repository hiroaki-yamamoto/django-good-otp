#!/usr/bin/env python
# coding=utf-8

"""Administration panel test."""

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode  # noqa

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # nonqa

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_otp.models import OTPSecrets
from django_otp.admin import OTPAdmin, AdminSite, OTPGenerationForm

from .bases import DBIntegrationTestBase


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


class AdminOTPGenerationFormTest(DBIntegrationTestBase, TestCase):
    """OTPGeneration form test."""

    def setUp(self):
        """Setup."""
        super(AdminOTPGenerationFormTest, self).setUp()
        self.form = OTPGenerationForm(instance=self.secret)

    def test_img_src(self):
        """The img source should be proper."""
        self.assertEqual(
            self.form.fields["secret"].widget.img_attrs["src"],
            reverse(
                "django_otp:qrcode", kwargs={"secret": self.secret.secret}
            ) + ("?{}").format(urlencode({"name": self.users[0].username}))
        )


class AdminOTPGenerationFormNoInstnaceTest(TestCase):
    """OTPGeneration form without model instancetest."""

    def setUp(self):
        """Setup."""
        self.form = OTPGenerationForm()

    def test_img_src(self):
        """The img source shouldn't be in the attr dict."""
        self.assertNotIn("src", self.form.fields["secret"].widget.img_attrs)
