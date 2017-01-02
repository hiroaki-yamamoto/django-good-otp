#!/usr/bin/env python
# coding=utf-8

"""Temporary views to check various variables."""

from django.views.generic import TemplateView
from django.utils.http import is_safe_url


class IndexView(TemplateView):
    """Index view."""

    template_name = "index.html"

    def is_safe_url(self, *args, **kwargs):
        """Check If the url is safe."""
        return is_safe_url(*args, **kwargs)
