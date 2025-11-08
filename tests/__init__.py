#!/usr/bin/env python
# coding=utf-8

"""Django OTP tests."""

import os

import django
from django.core.management import call_command


# Ensure Django can locate the bundled test settings before any Django modules
# are imported.  Several tests import project modules at module import time
# which in turn access ``django.conf.settings``.  When the environment variable
# is not defined beforehand Django raises ``ImproperlyConfigured`` during test
# collection.  Setting the default here mirrors what Django's ``manage.py``
# does and keeps the tests self-contained.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Trigger Django's setup so the app registry and translation infrastructure are
# ready for imports performed during test collection.
django.setup()

# Prepare the database schema.  The tests rely on Django's ORM and expect the
# built-in auth models to be present, so we run the migrations once when the
# test suite is imported.
call_command("migrate", run_syncdb=True, verbosity=0)
