#!/usr/bin/env python
# coding=utf-8

"""Views tests cases."""

try:
    from unittest.mock import ANY, patch
except ImportError:
    from mock import ANY, patch  # noqa

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from django_otp.views import QRCodeView

from .utils import gen_otp_secret


class QRCodeViewTest(TestCase):
    """QR code should be rendered properly."""

    @patch("django_otp.views.generate_qrcode")
    @patch("django_otp.views.build_otp_uri")
    def setUp(self, build_otp_uri, generate_qrcode):
        """Setup."""
        self.qrcode_data = "Good"

        def side_effect(stream):
            stream.write(self.qrcode_data.encode())

        generate_qrcode.return_value.save.side_effect = side_effect
        self.build_otp_uri = build_otp_uri
        self.generate_qrcode = generate_qrcode
        self.secret = gen_otp_secret()
        self.request = RequestFactory().get(
            reverse("qrcode", kwargs={"secret": self.secret})
        )
        self.view = QRCodeView.as_view()
        self.resp = self.view(self.request, self.secret)

    def test_status_code(self):
        """The status code should be 200."""
        self.assertEqual(self.resp.status_code, 200)

    def test_qrcode(self):
        """Qrcode generation function should be called as svg image."""
        from qrcode.image.svg import SvgPathImage as svg
        self.build_otp_uri.assert_called_once_with(self.secret)
        self.generate_qrcode.assert_called_once_with(
            self.build_otp_uri.return_value, image_factory=svg
        )
        self.generate_qrcode.return_value.save.assert_called_once_with(ANY)

    def test_content(self):
        """The content should be proper."""
        self.assertEqual(self.resp.content, self.qrcode_data.encode())
        self.assertEqual(
            self.resp["Content-Type"], ("image/svg+xml; charset={}").format(
                settings.DEFAULT_CHARSET
            )
        )
