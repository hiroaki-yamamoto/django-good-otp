#!/usr/bin/env python
# coding=utf-8

"""OTP related form."""

from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm
from django import forms
from django.utils.translation import ugettext_lazy as _lz


class AuthenticationForm(DjangoAuthForm):
    """Authentication form."""

    otp_auth = forms.IntegerField(
        label=_lz("2 FA Code"),
        max_value=999999, required=False
    )
