#!/usr/bin/env python
# coding=utf-8

"""OTP widgets tests."""

try:
    from unittest.mock import patch, call
except ImportError:
    from mock import patch, call

from django import setup
from django.test import TestCase

from django_otp.widgets import OTPGenWidget

setup()


class OTPGenWidgetInitWithoutAttrTest(TestCase):
    """OTP Generator Widget Init Test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, loader, env):
        """Setup."""
        self.widget = OTPGenWidget()
        self.loader = loader
        self.env = env

    def test_param_txt(self):
        """OTP Text Input attributes should be empty."""
        self.assertDictEqual({}, self.widget.attrs)

    def test_param_img(self):
        """OTP Image attributes should be empty."""
        self.assertDictEqual({}, self.widget.img_attrs)

    def test_img_flag(self):
        """By default, self.enable_img should be True."""
        self.assertTrue(self.widget.enable_img)

    def test_btn_flag(self):
        """By default, self.enable_btn should be True."""
        self.assertTrue(self.widget.enable_btn)

    def test_btn_attr(self):
        """Button argument should be empty."""
        self.assertDictEqual({"type": "button"}, self.widget.btn_attrs)

    def test_btn_label(self):
        """Button label should be 'Generate Secret'."""
        self.assertEqual(self.widget.btn_label, "Generate Secret")

    def test_template(self):
        """Check template load."""
        ret = self.widget.template
        self.loader.assert_called_once_with(
            "django_otp.widgets.otp_gen", "files"
        )
        self.env.assert_called_once_with(loader=self.loader.return_value)
        self.assertEqual(self.env.return_value.get_template.call_count, 3)
        self.env.return_value.get_template.has_calls((
            call("img.html"), call("button.html"), call("widget.html")
        ))
        self.assertIs(ret, self.env.return_value.get_template.return_value)


class OTPGenWidgetInitWithTextAttrTest(TestCase):
    """OTP Generator Widget Init with text attr test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, *args):
        """Setup."""
        self.txt_attrs = {"data-ng-model": "model.secret"}
        self.widget = OTPGenWidget(attrs={"data-ng-model": "model.secret"})

    def test_param_txt(self):
        """OTP text input attrs should be proper."""
        self.assertDictEqual(self.widget.attrs, self.txt_attrs)


class OTPGenWidgetInitWithImgAttrTest(TestCase):
    """OTP Generator Init with img attr test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, *args):
        """Setup."""
        self.img_attrs = {"data-ng-src": "{{ model.secret }}"}
        self.widget = OTPGenWidget(img_attrs=self.img_attrs)

    def test_param_img(self):
        """OTP image input attrs should be proper."""
        self.assertDictEqual(self.img_attrs, self.widget.img_attrs)


class OTPgenWidgetButtonAttrTest(TestCase):
    """OTPGenerator init with button attr test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, *args):
        """Setup."""
        self.btn_attrs = {"data-ng-click": "test()", "type": "button"}
        self.widget = OTPGenWidget(btn_attrs=self.btn_attrs)

    def test_btn_attr(self):
        """Button argument should be proper."""
        self.assertDictEqual(self.btn_attrs, self.widget.btn_attrs)

    def test_btn_label(self):
        """Button label should be 'Generate Secret'."""
        self.assertEqual(self.widget.btn_label, "Generate Secret")


class OTPgenWidgetButtonLabelTest(TestCase):
    """OTPGenerator init with button attr test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, *args):
        """Setup."""
        self.btn_label = "Hello World"
        self.widget = OTPGenWidget(btn_label=self.btn_label)

    def test_btn_label(self):
        """Button label should be 'Generate Secret'."""
        self.assertEqual(self.widget.btn_label, self.btn_label)


class OTPGenWidgetInitImgDiasbledTest(TestCase):
    """OTPGenerator init with image disabled test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, *args):
        """Setup."""
        self.widget = OTPGenWidget(enable_img=False)

    def test_img_flag(self):
        """enable_img flag should be false."""
        self.assertFalse(self.widget.enable_img)


class OTPGenWidgetBtnDisabledTest(TestCase):
    """OTPGenerator with btn disable test."""

    @patch("django_otp.widgets.otp_gen.Environment")
    @patch("django_otp.widgets.otp_gen.PackageLoader")
    def setUp(self, *args):
        """Setup."""
        self.widget = OTPGenWidget(enable_btn=False)

    def test_btn_flag(self):
        """By default, self.enable_btn should be False."""
        self.assertFalse(self.widget.enable_btn)
