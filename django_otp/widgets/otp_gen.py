#!/usr/bin/env python
# coding=utf-8

"""OTP Generator Widget."""

from django.forms.widgets import TextInput

from jinja2 import Environment, PackageLoader


class OTPGenWidget(TextInput):
    """OTP Generator widget."""

    def __init__(self, *args, **kwargs):
        """Init the instance."""
        self.img_attrs = kwargs.pop("img_attrs", None) or {}
        self.btn_attrs = kwargs.pop("btn_attrs", None) or {}
        self.btn_label = kwargs.pop("btn_label", None) or "Generate Secret"
        self.enable_img = bool(kwargs.pop("enable_img", True))
        self.enable_btn = bool(kwargs.pop("enable_btn", True))
        self.__env = Environment(loader=PackageLoader(__name__, "files"))
        self.template = self.__env.get_template("widget.html")
        self.btn_attrs.setdefault("type", "button")
        super(OTPGenWidget, self).__init__(*args, **kwargs)
