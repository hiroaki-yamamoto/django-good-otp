#!/usr/bin/env python
# coding=utf-8

"""URL routings."""

from django.conf.urls import url, include

urlpatterns = (
    url(r"", include("django_otp.urls")),
)
