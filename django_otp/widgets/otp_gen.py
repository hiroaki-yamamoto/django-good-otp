#!/usr/bin/env python
# coding=utf-8

"""OTP Generator Widget."""

from django.forms.widgets import TextInput


class OTPGenWidget(TextInput):
    """OTP Generator widget."""

    def __init__(self, *args, **kwargs):
        """Init the instance."""
        self.img_attrs = kwargs.pop("img_attrs", None) or {}
        self.btn_attrs = kwargs.pop("btn_attrs", None) or {}
        self.enable_img = bool(kwargs.pop("enable_img", True))
        super(OTPGenWidget, self).__init__(*args, **kwargs)
