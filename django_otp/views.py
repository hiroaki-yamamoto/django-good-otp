#!/usr/bin/env python
# coding=utf-8

"""Views."""

from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django.utils.translation import ugettext as _

from pyotp.utils import build_uri as build_otp_uri
from qrcode import make as generate_qrcode
from qrcode.image.svg import SvgPathImage as svg


class QRCodeView(View):
    """QRCode view."""

    def get(self, req, secret):
        """GET request."""
        result = bytes()
        otp_uri_kwargs = {
            key: value for (key, value) in req.GET.items() if key in (
                "name", "issuer_name"
            )
        }
        otp_uri_kwargs.setdefault("name", _("Untitled"))
        with BytesIO() as stream:
            generate_qrcode(
                build_otp_uri(secret, **otp_uri_kwargs), image_factory=svg
            ).save(stream)
            result = stream.getvalue()
        return HttpResponse(
            result, content_type=("image/svg+xml; charset={}").format(
                settings.DEFAULT_CHARSET
            )
        )
