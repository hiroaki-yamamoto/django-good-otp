#!/usr/bin/env python
# coding=utf-8

"""Test bases."""

from django.contrib.auth import get_user_model

from django_otp.models import OTPSecrets
from .utils import gen_otp_secret

from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.views.generic import TemplateView


class DBIntegrationTestBase(object):
    """Database integration test base."""

    def setUp(self, *args, **kwargs):
        """Setup."""
        super(DBIntegrationTestBase, self).setUp(*args, **kwargs)
        self.users = [
            get_user_model().objects.create_user(
                username=("test_{}").format(counter),
                password=("pw_{}").format(counter)
            ) for counter in range(2)
        ]
        self.secret = OTPSecrets.objects.create(
            user=self.users[0], secret=gen_otp_secret()
        )


class URLAssignmentTestBase(object):
    """
    URL assignment test base.
    Required/optional attribute:
        endpoint (required): The endpoint. e.g. home:index
        page_url (required): The url associated with the endpoint. e.g. /
        url_kwargs: Any keyword arguments to be put to reverse function.
        url_args: Any arguments to be put to reverse function.
    """

    method = "get"
    url_kwargs = {}
    url_args = []

    def __init__(self, *args, **kwargs):
        """Setup."""
        self.request = getattr(RequestFactory(), self.method)(self.page_url)

        if not getattr(self, "view", None):
            self.view = self.view_cls.as_view()
        super(URLAssignmentTestBase, self).__init__(*args, **kwargs)

    def test_url(self):
        """The URL should be found in the app."""
        self.assertEqual(
            reverse(
                self.endpoint, args=self.url_args, kwargs=self.url_kwargs
            ), self.page_url
        )

    def test_assignment(self):
        """The view should be assigned to URL."""
        self.assertEqual(
            resolve(self.page_url).func.__name__, self.view.__name__
        )


class TemplateViewTestBase(URLAssignmentTestBase):
    """
    View test base.
    Required/optional attribute:
        template_name (required): The file name of the template file.
        content_type (optional): The type of content as MimeType. By default,
            this is set to text/html.
        view_cls (required): The view class.
        endpoint (required): The endpoint. e.g. home:index
        page_url (required): The url associated with the endpoint. e.g. /
    """

    method = "get"

    def test_class(self):
        """The view class should be a subclass of TemplateView."""
        self.assertTrue(issubclass(self.view_cls, TemplateView))

    def test_template(self):
        """The TemplateView should have proper template name."""
        self.assertEqual(self.view_cls.template_name, self.template_name)

    def test_content_type(self):
        """The content type should be expected."""
        self.assertEqual(
            self.view_cls.content_type,
            getattr(self, "content_type", None)
        )
