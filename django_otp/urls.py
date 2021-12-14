#!/usr/bin/env python
# coding=utf-8

"""URL routings."""

from django.urls import re_path
from .views import QRCodeView

app_name = "django_otp"
urlpatterns = (
    re_path(
        r"^qrcode/(?P<secret>[a-zA-Z2-7]{16})$",
        QRCodeView.as_view(), name="qrcode"
    ),
)
