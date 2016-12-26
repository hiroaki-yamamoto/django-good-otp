#!/usr/bin/env python
# coding=utf-8

"""OTP related form."""

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm
from django import forms
from django.utils.translation import ugettext_lazy as _lz


class AuthenticationForm(DjangoAuthForm):
    """Authentication form."""

    otp_auth = forms.CharField(
        label=_lz("2 FA Code"),
        max_length=6, required=False
    )

    def __new__(cls, *args, **kwargs):
        """Class creation control."""
        instance = super(AuthenticationForm, cls).__new__(cls)
        instance.error_messages["invalid_login"] = _lz(
            "Please enter a correct %(username)s, password, and 2FA code. "
            "Note that either or both fields may be case-sensitive."
        )
        return instance

    def clean(self):
        """Clean the data."""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        otp = self.cleaned_data.get("otp_auth")

        if username and password:
            self.user_cache = authenticate(
                username=username, password=password, otp_auth=otp
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
