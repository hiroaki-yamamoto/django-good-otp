#!/usr/bin/env python
# coding=utf-8

"""Test bases."""

from django.contrib.auth import get_user_model

from django_otp.models import OTPSecrets
from .utils import gen_otp_secret


class DBIntegrationTestBase(object):
    """Database integration test base."""

    def setUp(self, *args, **kwargs):
        """Set up."""
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
