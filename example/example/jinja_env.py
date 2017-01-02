#!/usr/bin/env python
# coding=utf-8

"""Jinja2 env."""

from jinja2 import Environment
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find
from django.core.urlresolvers import reverse, resolve
from django.urls import NoReverseMatch
from django.utils.translation import ugettext, ungettext


def __static_exists__(path):
    """Check whether the specified path exists on static file or not."""
    return bool(find(path, all=True))


def url_exists(endpoint):
    """Check if the url exists."""
    try:
        return bool(reverse(endpoint))
    except NoReverseMatch:
        return False


def jinja_options(**env):
    """Set jinja env."""
    environ = Environment(**env)
    environ.globals.update({
        "settings": settings,
        "static": staticfiles_storage.url,
        "static_exists": __static_exists__,
        "url": reverse,
        "url_exists": url_exists,
        "urlparse": urlparse,
        "resolve": resolve,
        "getattr": getattr,
        "_": ugettext,
        "_n": ungettext
    })
    return environ
