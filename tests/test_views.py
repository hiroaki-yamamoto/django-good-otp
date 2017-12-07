#!/usr/bin/env python
# coding=utf-8

"""Views tests cases."""

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    from unittest.mock import ANY, patch
except ImportError:
    from mock import ANY, patch  # noqa

import django
from django.conf import settings
from django.test import TestCase, RequestFactory

from django_otp.views import QRCodeView

from .utils import gen_otp_secret

if django.VERSION < (2, 0):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class QRCodeViewTestBase(TestCase):
    """QR Code view test base."""

    def setUp(self, build_otp_uri, generate_qrcode, **query_args):
        """Setup."""
        self.secret = gen_otp_secret()
        query_str = ("?" + urlencode(query_args)) if query_args else ""
        self.request = RequestFactory().get(
            reverse(
                "django_otp:qrcode",
                kwargs={"secret": self.secret}
            ) + query_str
        )
        self.view = QRCodeView.as_view()

        self.qrcode_data = "Good"

        def side_effect(stream):
            stream.write(self.qrcode_data.encode())

        generate_qrcode.return_value.save.side_effect = side_effect
        self.build_otp_uri = build_otp_uri
        self.generate_qrcode = generate_qrcode
        self.resp = self.view(self.request, self.secret)


class QRCodeViewTest(QRCodeViewTestBase):
    """QR code should be rendered properly."""

    @patch("django_otp.views.generate_qrcode")
    @patch("django_otp.views.build_otp_uri")
    def setUp(self, *args):
        """Setup."""
        super(QRCodeViewTest, self).setUp(*args)

    def test_status_code(self):
        """The status code should be 200."""
        self.assertEqual(self.resp.status_code, 200)

    def test_qrcode(self):
        """Qrcode generation function should be called as svg image."""
        from qrcode.image.svg import SvgPathImage as svg
        self.build_otp_uri.assert_called_once_with(
            self.secret, name="Untitled"
        )
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


class QRCodeViewWithNameTest(QRCodeViewTestBase):
    """Qrcode view test case when name exsits."""

    @patch("django_otp.views.generate_qrcode")
    @patch("django_otp.views.build_otp_uri")
    def setUp(self, *args):
        """Setup."""
        self.name = "Test Example"
        super(QRCodeViewWithNameTest, self).setUp(*args, name=self.name)

    def test_qrcode(self):
        """Qrcode generation function should be called as svg image."""
        from qrcode.image.svg import SvgPathImage as svg
        self.build_otp_uri.assert_called_once_with(self.secret, name=self.name)
        self.generate_qrcode.assert_called_once_with(
            self.build_otp_uri.return_value, image_factory=svg
        )
        self.generate_qrcode.return_value.save.assert_called_once_with(ANY)


class QRCodeViewWithIssuerNameTest(QRCodeViewTestBase):
    """Qrcode view test case when name exsits."""

    @patch("django_otp.views.generate_qrcode")
    @patch("django_otp.views.build_otp_uri")
    def setUp(self, *args):
        """Setup."""
        self.issuer_name = "Test Example"
        super(QRCodeViewWithIssuerNameTest, self).setUp(
            *args, issuer_name=self.issuer_name
        )

    def test_qrcode(self):
        """Qrcode generation function should be called as svg image."""
        from qrcode.image.svg import SvgPathImage as svg
        self.build_otp_uri.assert_called_once_with(
            self.secret, issuer_name=self.issuer_name, name="Untitled"
        )
        self.generate_qrcode.assert_called_once_with(
            self.build_otp_uri.return_value, image_factory=svg
        )
        self.generate_qrcode.return_value.save.assert_called_once_with(ANY)


class QRCodeViewWithNameAndIssuerTest(QRCodeViewTestBase):
    """Qrcode view test case when name exsits."""

    @patch("django_otp.views.generate_qrcode")
    @patch("django_otp.views.build_otp_uri")
    def setUp(self, *args):
        """Setup."""
        self.issuer_name = "Test Example"
        self.name = "Test Name"
        super(QRCodeViewWithNameAndIssuerTest, self).setUp(
            *args, issuer_name=self.issuer_name, name=self.name
        )

    def test_qrcode(self):
        """Qrcode generation function should be called as svg image."""
        from qrcode.image.svg import SvgPathImage as svg
        self.build_otp_uri.assert_called_once_with(
            self.secret, issuer_name=self.issuer_name, name=self.name
        )
        self.generate_qrcode.assert_called_once_with(
            self.build_otp_uri.return_value, image_factory=svg
        )
        self.generate_qrcode.return_value.save.assert_called_once_with(ANY)
