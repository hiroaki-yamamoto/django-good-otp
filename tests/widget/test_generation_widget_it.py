#!/usr/bin/env python
# coding=utf-8

"""Otp secret generator integration test."""

from django import setup
from django.test import TestCase

from django_otp.widgets import OTPGenWidget

from jinja2 import Environment, PackageLoader

setup()


class OTPGenWidgetTemplateLoadTest(TestCase):
    """OTPGenerator template load test."""

    def setUp(self):
        """Setup."""
        self.widget = OTPGenWidget()
        self.env = Environment(
            loader=PackageLoader("django_otp.widgets", "files")
        )
        self.env.globals.update({
            "btn": self.widget.btn,
            "img": self.widget.img
        })

    def test_template_load(self):
        """The template should be compiled properly."""
        self.assertEqual(
            self.widget.template.render(widget=self.widget),
            self.env.get_template("widget.html").render(widget=self.widget)
        )
