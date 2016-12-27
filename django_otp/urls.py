#!/usr/bin/env python
# coding=utf-8

"""URL routings."""

from django.conf.urls import url
from .views import QRCodeView

app_name = "django_otp"
urlpatterns = (
    url(
        r"^qrcode/(?P<secret>[a-zA-Z2-7]{16})$",
        QRCodeView.as_view(), name="qrcode"
    ),
)
