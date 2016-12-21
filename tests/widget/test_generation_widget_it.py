#!/usr/bin/env python
# coding=utf-8

"""Otp secret generator integration test."""

from django.test import TestCase

from django_otp.widgets import OTPGenWidget

from jinja2 import Environment, PackageLoader


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

    def test_render(self):
        """Render should compile the template and should return the result."""
        result = self.widget.render(
            "test", "test_value", {"data-hello": "world"}
        )
        self.assertIn("data-hello=\"world\"", result)
        self.assertIn("value=\"test_value\"", result)
        self.assertEqual(
            result,
            self.widget.template.render(
                widget=self.widget,
                attrs={"data-hello": "world", "value": "test_value"}
            )
        )


class OTPGenWidgetTemplateLoadWithoutValueTest(TestCase):
    """OTP Secret Generator widget without value test."""

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

    def test_render(self):
        """Render should compile the template and should return the result."""
        result = self.widget.render(
            "test", None, {"data-hello": "world"}
        )
        self.assertIn("data-hello=\"world\"", result)
        self.assertNotIn("value=\"test_value\"", result)
        self.assertEqual(
            result,
            self.widget.template.render(
                widget=self.widget,
                attrs={"data-hello": "world"}
            )
        )
