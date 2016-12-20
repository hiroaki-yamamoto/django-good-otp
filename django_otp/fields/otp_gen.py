#!/usr/bin/env python
# coding=utf-8

"""Django OTP Generator Secret Key Generator field."""

from django import forms

from ..widgets import OTPGenWidget


class OTPGenField(forms.fields.CharField):
    """OTP Secret key generator field."""

    def __init__(self, *args, **kwargs):
        """Init this."""
        kwargs.setdefault("widget", OTPGenWidget())
        super(OTPGenField, self).__init__(*args, **kwargs)

    @property
    def image(self):
        """
        Return the image tag.

        Note that this property doesn't generate QR-Code, it generates an img
        tag only.
        """
        return self.widget.img({"widget": self.widget})
