#!/usr/bin/env python
# coding=utf-8

"""OTP Generator Widget."""

from django.forms.widgets import TextInput


class OTPGenWidget(TextInput):
    """OTP Generator widget."""

    def __init__(self, *args, **kwargs):
        """Init the instance."""
        self.img_attrs = kwargs.pop("img_attrs", None) or {}
        super(OTPGenWidget, self).__init__(*args, **kwargs)
