#!/usr/bin/env python
# coding=utf-8

"""URL routings."""

from django.urls import path, include

urlpatterns = (
    path("", include("django_otp.urls")),
)
