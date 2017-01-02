#!/usr/bin/env python
# coding=utf-8

"""Temporary views to check various variables."""

from django.views.generic import TemplateView
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse

from django.contrib.auth.views import _get_login_redirect_url


class IndexView(TemplateView):
    """Index view."""

    template_name = "index.html"

    def is_safe_url(self, *args, **kwargs):
        """Check If the url is safe."""
        return is_safe_url(*args, **kwargs)

    def get_login_redirect_url(self):
        """Get login redirect url."""
        return _get_login_redirect_url(self.request, reverse("admin:index"))
