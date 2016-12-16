#!/usr/bin/env python
# coding=utf-8

"""OTP widgets tests."""


from django import setup
from django.test import TestCase

from django_otp.widgets import OTPGenWidget

setup()


class OTPGenWidgetInitWithoutAttrTest(TestCase):
    """OTP Generator Widget Init Test."""

    def setUp(self):
        """Setup."""
        self.widget = OTPGenWidget()

    def test_param_txt(self):
        """OTP Text Input attributes should be empty."""
        self.assertDictEqual({}, self.widget.attrs)

    def test_param_img(self):
        """OTP Image attributes should be empty."""
        self.assertDictEqual({}, self.widget.attrs)

    def test_img_flag(self):
        """By default, self.enable_img should be True."""
        self.assertTrue(self.widget.enable_img)


class OTPGenWidgetInitWithTextAttrTest(TestCase):
    """OTP Generator Widget Init with text attr test."""

    def setUp(self):
        """Setup."""
        self.txt_attrs = {"data-ng-model": "model.secret"}
        self.widget = OTPGenWidget(attrs={"data-ng-model": "model.secret"})

    def test_param_txt(self):
        """OTP text input attrs should be proper."""
        self.assertDictEqual(self.widget.attrs, self.txt_attrs)

    def test_param_img(self):
        """OTP Image attributes should be empty."""
        self.assertDictEqual({}, self.widget.img_attrs)


class OTPGenWidgetInitWithImgAttrTest(TestCase):
    """OTP Generator Init with img attr test."""

    def setUp(self):
        """Setup."""
        self.img_attrs = {"data-ng-src": "{{ model.secret }}"}
        self.widget = OTPGenWidget(img_attrs=self.img_attrs)

    def text_param_txt(self):
        """OTP text input attrs should be empty."""
        self.assertDictEqual({}, self.widget.attrs)

    def test_param_img(self):
        """OTP image input attrs should be proper."""
        self.assertDictEqual(self.img_attrs, self.widget.img_attrs)


class OTPGenWidgetInitWithBothAttrTest(TestCase):
    """OTP Generator init with img and txt attrs test."""

    def setUp(self):
        """Setup."""
        self.img_attrs = {"data-ng-src": "{{ model.secret }}"}
        self.txt_attrs = {"data-ng-model": "model.secret"}
        self.widget = OTPGenWidget(
            img_attrs=self.img_attrs, attrs=self.txt_attrs
        )

    def test_param_txt(self):
        """OTP text input attrs should be proper."""
        self.assertDictEqual(self.widget.attrs, self.txt_attrs)

    def test_param_img(self):
        """OTP image input attrs should be proper."""
        self.assertDictEqual(self.img_attrs, self.widget.img_attrs)


class OTPGenWidgetInitImgDiasbledTest(TestCase):
    """OTPGenerator init with image disabled test."""

    def setUp(self):
        """Setup."""
        self.widget = OTPGenWidget(enable_img=False)

    def test_img_flag(self):
        """enable_img flag should be false."""
        self.assertFalse(self.widget.enable_img)
