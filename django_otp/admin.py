#!/usr/bin/env python
# coding=utf-8

"""OTP Admin Panel."""

import re

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode  # noqa

from django.core.urlresolvers import reverse
from django.contrib import admin
from django import forms
from os import path
from .models import OTPSecrets
from .forms import AuthenticationForm
from .widgets import OTPGenWidget


class OTPGenerationForm(forms.ModelForm):
    """OTP generation form."""

    class Meta(object):
        """Metadata."""

        model = OTPSecrets
        fields = ("user", "secret")
        widgets = {
            "secret": OTPGenWidget(embed_script=True, attrs={
                "class": "secret"
            })
        }

    def __init__(self, *args, **kwargs):
        """Init the instance."""
        super(OTPGenerationForm, self).__init__(*args, **kwargs)
        self.fields["secret"].widget.btn_attrs["onclick"] = (
            "assignOTPSecret("
            "'#{0}', '#{1}_container .secret', '#{1}_container .qrcode', '{2}'"
            ");"
        ).format(
            self["user"].id_for_label,
            self["secret"].id_for_label,
            re.sub(r"/A{16}$", "", reverse(
                "django_otp:qrcode",
                kwargs={"secret": "AAAAAAAAAAAAAAAA"}
            ))
        )
        self.fields["secret"].widget.img_attrs.setdefault("class", "")
        self.fields["secret"].widget.img_attrs["class"] += " qrcode"
        if self.instance.secret:
            self.fields["secret"].widget.img_attrs["src"] = reverse(
                "django_otp:qrcode", kwargs={"secret": self.instance.secret}
            ) + ("?{}").format(urlencode({
                "name": self.instance.user.username
            }))


class OTPAdmin(admin.ModelAdmin):
    """OTPSecret Admin."""

    list_display = ("user", )
    search_fields = (
        "user__email", "user__first_name", "user__last_name",
        "user__username"
    )
    form = OTPGenerationForm

    @classmethod
    def enable(cls):
        """Assign the model to the panel."""
        admin.site.register(OTPSecrets, cls)


class AdminSite(admin.AdminSite):
    """AdminSite."""

    login_form = AuthenticationForm
    login_template = path.join(
        path.abspath(path.dirname(__file__)),
        "templates", "1_10", "login.html"
    )

    def __init__(self, *args, **kwargs):
        """Initialize the instance."""
        inherit = bool(kwargs.pop("inherit_panels", True))
        super(AdminSite, self).__init__(*args, **kwargs)
        if inherit:
            self._registry = admin.site._registry.copy()
