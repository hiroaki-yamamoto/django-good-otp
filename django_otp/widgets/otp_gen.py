#!/usr/bin/env python
# coding=utf-8

"""OTP Generator Widget."""

from copy import copy
from django.forms.widgets import TextInput
from django.forms.utils import flatatt
from django.utils.translation import ugettext as _

from jinja2 import Environment, PackageLoader


class OTPGenWidget(TextInput):
    """OTP Generator widget."""

    def __init__(self, *args, **kwargs):
        """
        Init the instance.

        Keyword Arguments:
            img_attrs: The attribute of the image.
            btn_attrs: The attribute of 'generate new secret' button.
            btn_label: The label of new secret key generation button.
            enable_img: Set false not to render img tag.
            enable_btn: Set false not to render 'generate new secret' button.
            embed_script: Set true to embed scrpt. Setting this flag to true
                is useful when you use this widget in admin panel.
        """
        self.img_attrs = kwargs.pop("img_attrs", None) or {}
        self.btn_attrs = kwargs.pop("btn_attrs", None) or {}
        self.btn_label = kwargs.pop("btn_label", None) or _("Generate Secret")
        self.enable_img = bool(kwargs.pop("enable_img", True))
        self.enable_btn = bool(kwargs.pop("enable_btn", True))
        self.embed_script = bool(kwargs.pop("embed_script", False))
        self.__env = Environment(loader=PackageLoader(__name__, "files"))
        self.img = self.__env.get_template("img.html").render
        self.btn = self.__env.get_template("button.html").render
        self.btn_attrs.setdefault("type", "button")
        self.script = self.__env.get_template("assets.js").render
        self.__env.globals.update({
            "img": self.img,
            "btn": self.btn,
            "script": self.script,
            "build_attrs": self.build_attrs,
            "flatatt": flatatt
        })
        self.template = self.__env.get_template("widget.html")
        super(OTPGenWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        """Render the widegt."""
        additional_attrs = copy(attrs)
        additional_attrs["name"] = name
        if value is not None:
            additional_attrs.setdefault("value", value)
        return self.template.render({
            "widget": self, "attrs": additional_attrs
        })
