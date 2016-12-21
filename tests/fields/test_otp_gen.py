#!/usr/bin/env python
# coding=utf-8

"""OTP Secret key generator field."""

from django.test import TestCase

from django.forms import Form

from django_otp.fields import OTPGenField
from django_otp.widgets import OTPGenWidget


class OTPGenFieldTestBase(object):
    """OTP secret key generator test base."""

    def setUp(self):
        """Setup."""
        self.form = self.Form()

    def test_img(self):
        """The field should have image property that should be qr code."""
        self.assertEqual(
            self.form.fields["gen"].image,
            self.form.fields["gen"].widget.img({
                "widget": self.form.fields["gen"].widget
            })
        )


class OTPGenFieldWithoutAnyParamTest(OTPGenFieldTestBase, TestCase):
    """OTP secret key generator without any parameters test."""

    class Form(Form):
        """Form."""

        gen = OTPGenField()


class OTPGenFieldWithImgTest(OTPGenFieldTestBase, TestCase):
    """OTP secret key generator without any parameters test."""

    class Form(Form):
        """Form."""

        gen = OTPGenField(widget=OTPGenWidget(
            img_attrs={"data-ng-src": "{{ model.qrcode }}"}
        ))
